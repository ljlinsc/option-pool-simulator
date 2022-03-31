from dataclasses import dataclass
from enum import Enum, auto

class TransactionAction(Enum):
    # for liquidity providers
    DEPOSIT = auto()
    WITHDRAW = auto()

    # for purchasers
    BUY = auto()
    EXERCISE = auto()

@dataclass
class Transaction:
    epoch: int
    action: TransactionAction
    value: float
