from dataclasses import dataclass

@dataclass
class Epoch:
    start_date: str
    total_value_locked: float   # total value locked in the pool at the end of
                                # the epoch
    total_profit: float         # difference between the epoch's deposits and
                                # the epoch's withdrawls
