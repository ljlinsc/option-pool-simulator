import numpy as np
from simulation.option_pool import OptionPool
from data_classes.transaction import Asset


class LiquidityProvider:
    def __init__(self, option_pool: OptionPool) -> None:
        self.option_pool = option_pool
        self.profit = 0

    def start_epoch(self, date: str) -> None:
        self.option_pool.deposit(
            self.generateRandomDepositValue(),
            Asset.ETH
        )

    def end_epoch(self, date: str) -> None:
        self.option_pool.withdraw(
            self.generateRandomWithdrawValue(),
            Asset.ETH
        )

    def generateRandomDepositValue(self) -> float:
        # uniform distribution
        s = np.random.uniform(low=1, high=3)

        self.profit -= s
        return s

    def generateRandomWithdrawValue(self) -> float:
        # uniform distribution
        s = np.random.uniform(low=0, high=2)

        self.profit += s
        return s
