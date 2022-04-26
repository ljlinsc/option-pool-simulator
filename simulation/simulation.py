import random
from typing import List
from data_classes.distribution import Distribution
from processors.csv_processor import CSVProcessor

from simulation.liquidity_provider import LiquidityProvider
from simulation.option_pool import OptionPool
from simulation.purchaser import Purchaser


class Simulation:
    def __init__(
        self,
        csv_processor: CSVProcessor,
        num_liquidity_providers: int,
        num_purchasers: int,
        epoch_dates: List[str],
        purchaser_distribution: Distribution,
        lp_distribution: Distribution
    ) -> None:
        self.csv_processor = csv_processor
        self.epoch_dates = epoch_dates
        self.purchaser_distribution = purchaser_distribution
        self.lp_distribution = lp_distribution
        self.option_pool = OptionPool(csv_processor)
        self.actors = []

        # Create liquidity providers
        for i in range(num_liquidity_providers):
            self.actors.append(LiquidityProvider(
                self.csv_processor,
                self.option_pool,
                self.lp_distribution
            ))

        # Create purchasers
        for i in range(num_purchasers):
            self.actors.append(Purchaser(
                i,
                self.csv_processor,
                self.option_pool,
                self.purchaser_distribution
            ))

    def run(self) -> OptionPool:
        # Run simulation
        for i in range(0, len(self.epoch_dates) - 1):
            start_date = self.epoch_dates[i]
            end_date = self.epoch_dates[i + 1]

            self.option_pool.initialize_epoch_statistics(start_date)

            # Each actor takes an action at the start of the epoch
            random.shuffle(self.actors)
            for actor in self.actors:
                actor.start_epoch(start_date)

            # Each actor takes an action at the end of the epoch
            random.shuffle(self.actors)
            for actor in self.actors:
                actor.end_epoch(end_date)

            self.option_pool.unlock_underlying_assets()
            self.option_pool.convert_usdt_to_underlying_asset(end_date)
            self.option_pool.calculate_epoch_statistics()

        return self.option_pool
