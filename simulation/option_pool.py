from data_classes.option import Option, OptionType
from data_classes.transaction import Asset
from processors.csv_processor import CSVProcessor


class OptionPool:
    def __init__(self) -> None:
        self.total_underlying_asset = 0.0
        self.total_underlying_asset_locked = 0.0
        self.total_usdt = 0.0
        self.options = dict()
        self.csv_processor = CSVProcessor()
        self.end_of_epoch_tvls = []

    def deposit(self, value: float, asset: Asset) -> None:
        if asset == Asset.USDT:
            self.total_usdt += value
        else:
            self.total_underlying_asset += value

    def withdraw(self, value: float, asset: Asset) -> None:
        if asset == Asset.USDT:
            self.total_usdt -= value
        else:
            self.total_underlying_asset -= value

    def purchase_call_option(
        self,
        date: str,
        purchaser_id: int,
        option_index: int
    ) -> None:
        if self.total_underlying_asset - self.total_underlying_asset_locked > 0:
            '''
            If at least 1 of the underlying asset (e.g. 1 ETH) is available in
            the option pool, then that asset will be locked, and the Purchaser
            will pay the premium.
            '''
            strike = self.csv_processor.get_strike_price(date, option_index)
            premium = self.csv_processor.get_premium(date, option_index)
            self.total_underlying_asset_locked -= 1
            self.total_usdt += premium
            self.options[purchaser_id] = Option(
                OptionType.CALL,
                option_index,
                strike,
                premium
            )

    def exercise_call_option(self, date: str, purchaser_id: int) -> None:
        if purchaser_id in self.options.keys():
            strike = self.options.pop(purchaser_id).strike
            if strike <= self.csv_processor.get_end_eth_price(date):
                # Option is exercised
                self.total_underlying_asset -= 1
                self.total_underlying_asset_locked -= 1

    def convert_usdt_to_underlying_asset(self, date: str) -> None:
        end_eth_price = self.csv_processor.get_end_eth_price(date)
        self.total_underlying_asset += self.total_usdt / end_eth_price
        self.total_usdt = 0
        self.end_of_epoch_tvls.append(
            end_eth_price * self.total_underlying_asset)
