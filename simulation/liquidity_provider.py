from simulation.option_pool import OptionPool
from data_classes.transaction import Transaction, TransactionAction

class LiquidityProvider:
    def __init__(self, option_pool: OptionPool) -> None:
        self.option_pool = option_pool
        self.profit = 0

    def start_epoch(self, epoch: int) -> Transaction:
        return self.option_pool.execute_transaction(Transaction(
            epoch,
            TransactionAction.DEPOSIT,
            self.generateRandomDepositValue(),
        ))

    def end_epoch(self, epoch: int) -> Transaction:
        return self.option_pool.execute_transaction(Transaction(
            epoch,
            TransactionAction.WITHDRAW,
            self.generateRandomWithdrawValue(),
        ))

    def generateRandomDepositValue(self) -> float:
        # TODO
        # return 100.0

        # uniform distribution
        s = np.random.uniform(low=70.0, high=120.0)
        
        profit = profit - s
        return s


    def generateRandomWithdrawValue(self) -> float:
        # TODO
        # return 15.0

        # uniform distribution
        s = np.random.uniform(low=50.0, high=100.0)

        profit = profit + s
        return s
