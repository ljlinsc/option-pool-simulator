from epoch import Epoch
from transaction import Transaction, TransactionAction
from typing import List

class DataProcessor:
    def __init__(self, num_epochs: int, transactions: List[Transaction]) -> None:
        self.num_epochs = num_epochs
        self.transactions = transactions
    
    def getEpochs(self) -> List[Epoch]:
        epochs: List[Epoch] = [Epoch(i, 0.0, 0.0) for i in range(self.num_epochs)]

        # Total profit for each epoch
        for transaction in self.transactions:
            total_value = transaction.value * transaction.quantity
            if transaction.action == TransactionAction.DEPOSIT:
                epochs[transaction.epoch].total_profit += total_value
            elif transaction.action == TransactionAction.WITHDRAW:
                epochs[transaction.epoch].total_profit -= total_value
        
        # Total value locked at the end of each epoch
        epochs[0].total_value_locked = epochs[0].total_profit
        for i in range(1, self.num_epochs):
            epochs[i].total_value_locked = epochs[i - 1].total_value_locked + epochs[i].total_profit

        return epochs
