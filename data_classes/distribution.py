from enum import Enum, auto


# purchaser distributions
class PurchaserDist(Enum):
    UNIFORM = auto()
    NORMAL = auto()
    SKEWIN = auto()
    SKEWOUT = auto()


# liquidity provider distribution
class LPDist(Enum):
    UNIFORM = auto()


class Distribution:
    def __init__(self, purchaser_dist: PurchaserDist) -> None:
        self.purchaser_dist = purchaser_dist
        self.lp_dist = LPDist.UNIFORM
