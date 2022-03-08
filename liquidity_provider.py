from option_pool import OptionPool
from transaction import Transaction, TransactionAction

class LiquidityProvider:
    def __init__(self, option_pool: OptionPool) -> None:
        self.option_pool = option_pool

    def start_epoch(self, epoch: int) -> Transaction:
        return self.option_pool.execute_transaction(Transaction(
            epoch,
            TransactionAction.DEPOSIT,
            self.generateRandomDepositValue(),
            1
        ))

    def end_epoch(self, epoch: int) -> Transaction:
        return self.option_pool.execute_transaction(Transaction(
            epoch,
            TransactionAction.WITHDRAW,
            self.generateRandomWithdrawValue(),
            1
        ))

    def generateRandomDepositValue(self) -> float:
        # TODO
        return 100.0

    def generateRandomWithdrawValue(self) -> float:
        # TODO
        return 15.0
