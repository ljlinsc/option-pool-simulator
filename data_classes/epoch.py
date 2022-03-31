from dataclasses import dataclass

@dataclass
class Epoch:
    epoch: int                  # ordered identifier (e.g. the first epoch = 0)
    total_value_locked: float   # total value locked in the pool at the end of
                                # the epoch
    total_profit: float         # difference between the epoch's deposits and
                                # the epoch's withdrawls
