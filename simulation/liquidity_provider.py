import numpy as np
from data_classes.distribution import LPDistribution
from processors.csv_processor import CSVProcessor
from simulation.option_pool import OptionPool
from data_classes.transaction import Asset


class LiquidityProvider:
    def __init__(self, csv_processor: CSVProcessor, option_pool: OptionPool, distribution: LPDistribution) -> None:
        self.csv_processor = csv_processor
        self.option_pool = option_pool
        self.distribution = distribution
        self.num_eth_in_pool = 0

        # Statistics
        self.profit = 0
        self.num_eth_deposited = 0
        self.num_eth_withdrawn = 0

    def start_epoch(self, date: str) -> None:
        value = self.generate_random_deposit_value()
        self.option_pool.deposit(
            value,
            Asset.ETH
        )

        self.profit -= self.csv_processor.get_eth_price(date) * value
        self.num_eth_in_pool += value
        self.num_eth_deposited += value

    def end_epoch(self, date: str) -> None:
        value = self.generate_random_withdraw_value()
        if value >= self.num_eth_in_pool:
            is_success = self.option_pool.withdraw(
                value,
                Asset.ETH
            )
            if is_success:
                self.profit += self.csv_processor.get_eth_price(date) * value
                self.num_eth_in_pool -= 1
                self.num_eth_withdrawn += 1

    def generate_random_deposit_value(self) -> float:
        if self.distribution == LPDistribution.UNIFORM:
            return np.random.uniform(low=1, high=3)
        else:
            return 0.0

    def generate_random_withdraw_value(self) -> float:
        if self.distribution == LPDistribution.UNIFORM:
            return np.random.uniform(low=0, high=2)
        else:
            return 0.0
