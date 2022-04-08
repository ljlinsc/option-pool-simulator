from data_classes.epoch import Epoch
from data_classes.transaction import Transaction, TransactionAction
from typing import List

class DataProcessor:
    def __init__(self, epoch_dates: List[str], transactions: List[Transaction], size_of_pool: int) -> None:
        self.epoch_dates = epoch_dates
        self.transactions = transactions
        self.size_of_pool = size_of_pool
    
    def getEpochs(self) -> List[Epoch]:
        epochs: List[Epoch] = [Epoch(date, 0.0, 0.0) for date in self.epoch_dates]

        # Total profit for each epoch
        for transaction in self.transactions:
            if transaction.action == TransactionAction.DEPOSIT:
                epochs[self.getEpochIndex(epochs, transaction.date)].total_profit += transaction.value
            elif transaction.action == TransactionAction.WITHDRAW:
                epochs[self.getEpochIndex(epochs, transaction.date)].total_profit -= transaction.value
            elif transaction.action == TransactionAction.PURCHASE:
                epochs[self.getEpochIndex(epochs, transaction.date)].total_profit += transaction.value
            elif transaction.action == TransactionAction.EXERCISE:
                epochs[self.getEpochIndex(epochs, transaction.date)].total_profit -= transaction.value
        
        # Total value locked at the end of each epoch
        epochs[0].total_value_locked = epochs[0].total_profit
        for i in range(1, len(epochs)):
            epochs[i].total_value_locked = epochs[i - 1].total_value_locked + epochs[i].total_profit

        return epochs

    def getEpochIndex(self, epochs: List[Epoch], date: str) -> int:
        for i in range(len(epochs)):
            if (epochs[i].start_date == date):
                return i
        return -1
