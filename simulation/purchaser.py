from datetime import datetime

from data_classes.distribution import Distribution
from simulation.option_pool import OptionPool
from utils.csv_processor import CSVProcessor


class Purchaser:
    def __init__(
        self,
        id: int,
        csv_processor: CSVProcessor,
        option_pool: OptionPool,
        distribution: Distribution
    ) -> None:
        self.id = id
        self.csv_processor = csv_processor
        self.option_pool = option_pool
        self.distribution = distribution

        # Statistics
        self.profit = 0

    def start_epoch(self, date: datetime) -> None:
        premium = self.option_pool.purchase_call_option(
            date,
            self.id,
            self.generate_random_strike_range_value()
        )
        if premium != -1:
            self.profit -= premium

    def end_epoch(self, date: datetime) -> None:
        strike = self.option_pool.exercise_call_option(
            date,
            self.id
        )
        if strike != -1:
            self.profit -= strike
            self.profit += self.csv_processor.get_underlying_price(date)

    def generate_random_strike_range_value(self) -> float:
        '''
        Use self.distribution to randomly pick a float in the range [0, 1] where
        0 represents the most in-the-money strike price and 1 represents the
        most out-of-the-money strike price.
        '''
        return self.distribution.generate_value()
