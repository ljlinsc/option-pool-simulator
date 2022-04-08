import numpy as np

from simulation.option_pool import OptionPool
from data_classes.transaction import Transaction, TransactionAction

class Purchaser:
    def __init__(self, id: int, option_pool: OptionPool) -> None:
        self.id = id
        self.option_pool = option_pool
        self.profit = 0

    def start_epoch(self, date: str) -> Transaction:
        return self.option_pool.purchase_call_option(
            date,
            self.id,
            self.generateRandomOption()
        )


    def end_epoch(self, date: str) -> Transaction:
        return self.option_pool.exercise_call_option(
            date,
            self.id
        )

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


