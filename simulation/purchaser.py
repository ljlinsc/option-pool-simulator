from option_pool import OptionPool
from transaction import Transaction, TransactionAction

class Purchaser:
    def __init__(self, option_pool: OptionPool) -> None:
        self.option_pool = option_pool
        self.profit = 0

    def start_epoch(self, epoch: int) -> Transaction:
        return self.option_pool.execute_transaction(Transaction(
            epoch,
            TransactionAction.PURCHASE,
            self.generateRandomOption(),
            1
        ))


    def end_epoch(self, epoch: int) -> Transaction:
        return self.option_pool.execute_transaction(Transaction(
            epoch,
            TransactionAction.EXERCISE,
            self.exerciseOption(),
            1
        ))

    def generateRandomOption(self) -> float:
        # TO DO
        ''' 
            - search CSV file for 'current date'
            - retrieve 3 options, one in the money, 2 out the money
            - have purchaser pay for the premium
            - assign option to the purchaser
        '''
        return 0.0

    def exerciseOption(self) -> float:
        # TO DO
        '''
            - end of epoch, unassign option from purchaser
            - give/take purchaser profit from difference between current price and strike price
        '''
        return 0.0


