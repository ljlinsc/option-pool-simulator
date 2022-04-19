from scipy.stats import skewnorm, norm


import numpy as np
from data_classes.distribution import Distribution, PurchaserDist

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
        '''
        picking a number from [0, 58)... will change later to match the above
        '''

        # uniform distribution
        if self.distribution == PurchaserDist.UNIFORM:
            s = np.random.uniform(low=0, high=57)

        # normal distribution centered at the money
        elif self.distribution == PurchaserDist.NORMAL:
            s = norm(loc=28.5, scale=10.0).rvs()

        # normal distribution centered in the money
        elif self.distribution == PurchaserDist.SKEWIN:
            s = skewnorm(3, loc=10, scale=10.0).rvs()


        # normal distribution centered out the money
        elif self.distribution == PurchaserDist.SKEWOUT:
            s = skewnorm(-3, loc=46, scale=10.0).rvs()

        # fix out of range values
        if s < 0:
            s = 0
        elif s > 57:
            s = 57

        s = round(s, 0)

        return s
