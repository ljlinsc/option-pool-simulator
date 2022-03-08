from transaction import Transaction, TransactionAction

class OptionPool:
    def __init__(self, underlying_asset: str) -> None:
        self.underlying_asset = underlying_asset
        self.total_value_locked = 0.0
    
    def execute_transaction(self, transaction: Transaction) -> Transaction:
        if transaction.action == TransactionAction.DEPOSIT:
            self.total_value_locked += transaction.value * transaction.quantity
        elif transaction.action == TransactionAction.WITHDRAW:
            self.total_value_locked -= transaction.value * transaction.quantity
        return transaction
