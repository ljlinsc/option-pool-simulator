import random
from data_classes.distribution import Distribution

from simulation.option_pool import OptionPool


class Purchaser:
    def __init__(
        self,
        id: int,
        option_pool: OptionPool,
        distribution: Distribution
    ) -> None:
        self.id = id
        self.option_pool = option_pool
        self.distribution = distribution
        self.profit = 0

    def start_epoch(self, date: str) -> None:
        self.option_pool.purchase_call_option(
            date,
            self.id,
            self.generate_random_strike_range_value(),
            # TODO Remove after implementing strike price calculator
            self.generate_random_strike_range_value()
        )

    def end_epoch(self, date: str) -> None:
        self.option_pool.exercise_call_option(
            date,
            self.id
        )

    def generate_random_strike_range_value(self) -> float:
        '''
        TODO
        Use self.distribution to randomly pick a float in the range [0, 1] where
        0 represents the most in-the-money strike price and 1 represents the
        most out-of-the-money strike price.
        '''
        return random.randrange(58)  # FIXME
