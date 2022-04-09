from data_classes.option import Option, OptionType
from data_classes.transaction import Transaction, TransactionAction
from processors.csv_processor import CSVProcessor

class OptionPool:
    def __init__(self, underlying_asset: str) -> None:
        self.underlying_asset = underlying_asset
        self.total_value_locked = 0.0
        self.total_collateral_locked = 0.0
        self.options = dict() # maps the purchaser's id to their option
        self.csv_processor = CSVProcessor()
    
    def execute_transaction(self, transaction: Transaction) -> Transaction:
        if transaction.action == TransactionAction.DEPOSIT:
            self.total_value_locked += transaction.value
        elif transaction.action == TransactionAction.WITHDRAW:
            self.total_value_locked -= transaction.value
        return transaction

    def purchase_call_option(self, date: str, purchaser_id: int, option_num: int) -> Transaction:
        strike_price = self.csv_processor.get_strike_prices(date)[option_num]
        if self.total_value_locked - self.total_collateral_locked >= strike_price:
            premium = self.csv_processor.get_premium_prices(date)[option_num]
            self.total_value_locked += premium
            self.total_collateral_locked += strike_price
            self.options[purchaser_id] = Option(
                OptionType.CALL,
                strike_price,
                premium
            )
            return Transaction(
                date,
                TransactionAction.PURCHASE,
                premium
            )
        else:
            return Transaction(
                date,
                TransactionAction.REJECT,
                0.0
            )

    def exercise_call_option(self, date: str, purchaser_id: int) -> Transaction:
        if purchaser_id not in self.options.keys():
            return Transaction(
                date,
                TransactionAction.EXERCISE,
                0.0
            )
        strike_price = self.options[purchaser_id].strike_price
        self.total_collateral_locked -= strike_price
        self.options.pop(purchaser_id)

        if self.get_underlying_asset_price(date) >= strike_price:
            # Price of the underlying asset increases and the purchaser exercises
            self.total_value_locked -= strike_price
            return Transaction(
                date,
                TransactionAction.EXERCISE,
                strike_price
            )
        else:
            # Price of the underlying asset decreases and the purchaser does not exercise
            return Transaction(
                date,
                TransactionAction.EXERCISE,
                0.0
            )

    def get_underlying_asset_price(self, date: str) -> float:
        return self.csv_processor.get_end_underlying_asset_price(date)