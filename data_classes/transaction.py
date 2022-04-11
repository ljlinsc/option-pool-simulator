from dataclasses import dataclass
from enum import Enum, auto


class Asset(Enum):
    ETH = auto()
    USDT = auto()


class TransactionAction(Enum):
    # for liquidity providers
    DEPOSIT = auto()
    WITHDRAW = auto()

    # for purchasers
    PURCHASE = auto()
    EXERCISE = auto()


@dataclass
class Transaction:
    date: str
    action: TransactionAction
    asset: Asset
    value: float
