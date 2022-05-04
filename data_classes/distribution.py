from enum import Enum, auto
from scipy.stats import skewnorm, norm

import numpy as np


class PurchaserDistribution(Enum):
    UNIFORM = auto()
    NORMAL = auto()  # normal distribution centered at the money
    SKEWIN = auto()  # normal distribution centered in the money
    SKEWOUT = auto()  # normal distribution centered out the money
    EXTREMESKEWIN = auto()  # normal distribution centered extremely in the money
    EXTREMESKEWOUT = auto()  # normal distribution centered extremely out the money


class LPDistribution(Enum):
    UNIFORM = auto()
    NORMAL = auto()
    SKEWIN = auto()
    SKEWOUT = auto()


class Distribution:
    def __init__(self, distribution: PurchaserDistribution or LPDistribution) -> None:
        self.distribution = distribution
        if distribution == PurchaserDistribution.UNIFORM:
            self.name = "Uniform"
        elif distribution == PurchaserDistribution.NORMAL:
            self.name = "Normal"
        elif distribution == PurchaserDistribution.SKEWIN:
            self.name = "Skewed in the money"
        elif distribution == PurchaserDistribution.SKEWOUT:
            self.name = "Skewed out of the money"
        elif distribution == PurchaserDistribution.EXTREMESKEWIN:
            self.name = "Skewed extremely in the money"
        elif distribution == PurchaserDistribution.EXTREMESKEWOUT:
            self.name = "Skewed extremely out of the money"

        elif distribution == LPDistribution.UNIFORM:
            self.name = "Uniform"
        elif distribution == LPDistribution.NORMAL:
            self.name = "Normal"

        else:
            raise NotImplementedError

    def generate_value(self) -> float:
        if self.distribution == PurchaserDistribution.UNIFORM:
            return self.fix_range(np.random.uniform(low=0, high=1))
        elif self.distribution == PurchaserDistribution.NORMAL:
            return self.fix_range(norm(loc=0.5, scale=0.2).rvs())
        elif self.distribution == PurchaserDistribution.SKEWIN:
            return self.fix_range(skewnorm(3, loc=0.2, scale=0.2).rvs())
        elif self.distribution == PurchaserDistribution.SKEWOUT:
            return self.fix_range(skewnorm(-3, loc=0.8, scale=0.2).rvs())
        elif self.distribution == PurchaserDistribution.EXTREMESKEWIN:
            return self.fix_range(skewnorm(9, loc=0.05, scale=0.2).rvs())
        elif self.distribution == PurchaserDistribution.EXTREMESKEWOUT:
            return self.fix_range(skewnorm(-9, loc=0.95, scale=0.2).rvs())

        return 0.0

    def generate_ranged_value(self, low: float, high: float) -> float:
        if self.distribution == LPDistribution.UNIFORM:
            return np.random.uniform(low=low, high=high)
        elif self.distribution == LPDistribution.NORMAL:
            return norm(loc=(high + low)/2., scale=(high - low)/4.).rvs()

        return 0.0

    def fix_range(self, value: float) -> float:
        if value < 0:
            return 0
        elif value > 1:
            return 1
        return value
