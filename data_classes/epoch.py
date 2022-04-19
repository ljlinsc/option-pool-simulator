from dataclasses import dataclass
from typing import List


@dataclass
class Epoch:
    start_date: str

    end_eth_price: float

    # total value locked in the pool at the end of the epoch
    total_value_locked: float

    # difference between the epoch's deposits and the epoch's withdrawls
    total_profit: float

    # difference between the epoch's premiums and exercises
    total_lp_profit: float
