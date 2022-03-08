from enum import Enum, auto

class TransactionAction(Enum):
    DEPOSIT = auto()
    WITHDRAW = auto()

class Transaction:
    def __init__(self, epoch: int, action: TransactionAction, value: float, quantity: int) -> None:
        self.epoch = epoch
        self.action = action
        self.value = value
        self.quantity = quantity
