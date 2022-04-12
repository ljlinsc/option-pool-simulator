from data_classes.epoch import Epoch
from data_classes.option import Option, OptionType
from data_classes.transaction import Asset
from processors.csv_processor import CSVProcessor


class OptionPool:
    def __init__(self) -> None:
        self.total_underlying_asset_unlocked = 0.0
        self.total_underlying_asset_locked = 0.0
        self.total_usdt = 0.0
        self.options = dict()
        self.csv_processor = CSVProcessor()
        self.epochs = []

    def deposit(self, value: float, asset: Asset) -> None:
        if asset == Asset.USDT:
            self.total_usdt += value
        else:
            self.total_underlying_asset_unlocked += value

    def withdraw(self, value: float, asset: Asset) -> None:
        if asset == Asset.USDT:
            if self.total_usdt >= value:
                self.total_usdt -= value
        else:
            if self.total_underlying_asset_unlocked >= value:
                self.total_underlying_asset_unlocked -= value

    def purchase_call_option(
        self,
        date: str,
        purchaser_id: int,
        option_index: int,  # TODO Remove after implementing strike price calculator
        value: float
    ) -> None:
        if self.total_underlying_asset_unlocked > 0:
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

            # Lock the underlying asset
            self.total_underlying_asset_unlocked -= 1
            self.total_underlying_asset_locked += 1

            # Pay the premium
            self.total_usdt += premium

            # Store the option details
            self.options[purchaser_id] = Option(
                OptionType.CALL,
                option_index,
                strike,
                premium
            )

            # Epoch statistics
            self.epochs[-1].total_lp_profit += premium

    def exercise_call_option(self, date: str, purchaser_id: int) -> None:
        if purchaser_id in self.options.keys():
            strike = self.options.pop(purchaser_id).strike
            if strike <= self.csv_processor.get_end_eth_price(date):
                # Option is exercised
                self.total_underlying_asset_locked -= 1
                self.epochs[-1].total_lp_profit -= self.epochs[-1].end_eth_price

    def unlock_underlying_assets(self) -> None:
        self.total_underlying_asset_unlocked += self.total_underlying_asset_locked
        self.total_underlying_asset_locked = 0.0

    def convert_usdt_to_underlying_asset(self, date: str) -> None:
        self.total_underlying_asset_unlocked += self.total_usdt / \
            self.csv_processor.get_end_eth_price(date)
        self.total_usdt = 0

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

    def initialize_epoch_statistics(self, date: str) -> None:
        self.epochs.append(Epoch(
            date,
            self.csv_processor.get_end_eth_price(date),
            0.0,
            0.0,
            0.0
        ))

    def calculate_epoch_statistics(self) -> None:
        # Calculate the total value locked in the option pool (USDT)
        self.epochs[-1].total_value_locked = self.epochs[-1].end_eth_price * \
            self.total_underlying_asset_unlocked

        # Calculate the total profit of the option pool (USDT)
        if len(self.epochs) == 1:
            self.epochs[-1].total_profit = self.epochs[-1].total_value_locked
        else:
            self.epochs[-1].total_profit = self.epochs[-1].total_value_locked - \
                self.epochs[-2].total_value_locked
