from dataclasses import dataclass
from enum import Enum, auto

class TransactionAction(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()

@dataclass
class Transaction:
    epoch: int
    action: TransactionAction
    value: float
