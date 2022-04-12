from data_classes.epoch import Epoch
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
        self.epochs = []

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
        option_index: int,  # TODO Remove after implementing strike price calculator
        value: float
    ) -> None:
        if self.total_underlying_asset - self.total_underlying_asset_locked > 0:
            '''
            If at least 1 of the underlying asset (e.g. 1 ETH) is available in
            the option pool, then that asset will be locked, and the Purchaser
            will pay the premium.
            '''
            strike = self.calculate_strike_price(
                value,
                date,
                option_index  # TODO Remove after implementing strike price calculator
            )
            premium = self.calculate_premium(
                date,
                strike,
                option_index  # TODO Remove after implementing strike price calculator
            )
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

    def calculate_epoch_statistics(self, date: str) -> None:
        end_eth_price = self.csv_processor.get_end_eth_price(date)
        total_value_locked = end_eth_price * self.total_underlying_asset
        if len(self.epochs) == 0:
            total_profit = total_value_locked
        else:
            total_profit = total_value_locked - \
                self.epochs[-1].total_value_locked
        self.epochs.append(Epoch(
            date,
            total_value_locked,
            total_profit
        ))

    def calculate_lowest_strike(self, date: str) -> float:
        return 0.0  # TODO

    def calculate_highest_strike(self, date: str) -> float:
        return 0.0  # TODO

    def calculate_strike_price(
        self,
        value: float,
        date: str,
        option_index: int  # TODO Remove after implementing strike price calculator
    ) -> float:
        '''
        TODO
        Given a value in the range [0, 1] where 0 is the lowest possible strike
        price and 1 is the highest possible strike price, return the
        corresponding strike price.
        '''
        return self.csv_processor.get_strike_price(date, option_index)  # FIXME

    def calculate_premium(
        self,
        date: str,
        strike: float,
        option_index: int  # TODO Remove after implementing strike price calculator
    ) -> float:
        '''
        TODO
        Given a date and a strike price, calculate the price of the option
        premium in USDT based on values from the CSVs.
        '''
        return self.csv_processor.get_premium(date, option_index)  # FIXME
