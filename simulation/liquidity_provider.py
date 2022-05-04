from datetime import datetime

from data_classes.distribution import Distribution
from data_classes.underlying_asset import UnderlyingAsset
from utils.csv_processor import CSVProcessor
from simulation.option_pool import OptionPool


class LiquidityProvider:
    def __init__(
        self,
        csv_processor: CSVProcessor,
        option_pool: OptionPool,
        distribution: Distribution,
        asset: UnderlyingAsset
    ) -> None:
        self.csv_processor = csv_processor
        self.option_pool = option_pool
        self.distribution = distribution
        self.asset = asset
        self.num_underlying_in_pool = 0

        # Statistics
        self.profit = 0
        self.num_underlying_deposited = 0
        self.num_underlying_withdrawn = 0

    def start_epoch(self, date: datetime) -> None:
        value = self.generate_random_deposit_value()
        self.option_pool.deposit(
            value,
            self.asset
        )

        self.profit -= self.csv_processor.get_underlying_price(date) * value
        self.num_underlying_in_pool += value
        self.num_underlying_deposited += value

    def end_epoch(self, date: datetime) -> None:
        value = self.generate_random_withdraw_value()
        if value >= self.num_underlying_in_pool:
            is_success = self.option_pool.withdraw(
                value,
                self.asset
            )
            if is_success:
                self.profit += self.csv_processor.get_underlying_price(
                    date) * value
                self.num_underlying_in_pool -= 1
                self.num_underlying_withdrawn += 1

    def generate_random_deposit_value(self) -> float:
        return self.distribution.generate_ranged_value(1, 3)

    def generate_random_withdraw_value(self) -> float:
        return self.distribution.generate_ranged_value(0, 2)
