import random
from typing import List
from data_classes.distribution import Distribution

from simulation.liquidity_provider import LiquidityProvider
from simulation.option_pool import OptionPool
from simulation.purchaser import Purchaser


class Simulation:
    def __init__(
        self,
        num_liquidity_providers: int,
        num_purchasers: int,
        epoch_dates: List[str],
        purchaser_distribution: Distribution
    ) -> None:
        self.actors = []
        self.option_pool = OptionPool()
        self.epoch_dates = epoch_dates
        self.purchaser_distribution = purchaser_distribution

        # Create liquidity providers
        for i in range(num_liquidity_providers):
            self.actors.append(LiquidityProvider(self.option_pool))

        # Create purchasers
        for i in range(num_purchasers):
            self.actors.append(
                Purchaser(i, self.option_pool, self.purchaser_distribution)
            )

    def run(self) -> OptionPool:
        # Run simulation
        for date in self.epoch_dates:
            # Each actor takes an action at the start of the epoch
            random.shuffle(self.actors)
            for actor in self.actors:
                actor.start_epoch(date)

            # Each actor takes an action at the end of the epoch
            random.shuffle(self.actors)
            for actor in self.actors:
                actor.end_epoch(date)

            # Remaining USDT in the option pool is converted to the underlying
            self.option_pool.convert_usdt_to_underlying_asset(date)

            # Calculate end of the epoch statistics
            self.option_pool.calculate_epoch_statistics(date)

        return self.option_pool
