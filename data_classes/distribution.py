from enum import Enum, auto


# purchaser distributions
class PurchaserDistribution(Enum):
    UNIFORM = auto()
    NORMAL = auto()
    SKEWIN = auto()
    SKEWOUT = auto()


# liquidity provider distribution
class LPDistribution(Enum):
    UNIFORM = auto()


class Distribution:
    def __init__(self, purchaser_distribution: PurchaserDistribution, lp_distribution: LPDistribution) -> None:
        self.purchaser_distribution = purchaser_distribution
        self.lp_distribution = lp_distribution
