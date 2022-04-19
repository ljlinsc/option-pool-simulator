import numpy as np
from scipy.stats import norm
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
        self.strike_values = []
        self.strikes = []
        self.premiums = []

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
        value: float
    ) -> None:
        if self.total_underlying_asset_unlocked > 0:
            strike = self.calculate_strike_price(
                value,
                date,
            )
            premium = self.calculate_premium(
                date,
                strike,
            )

            # Lock the underlying asset
            self.total_underlying_asset_unlocked -= 1
            self.total_underlying_asset_locked += 1

            # Pay the premium
            self.total_usdt += premium

            # Store the option details
            self.options[purchaser_id] = Option(
                OptionType.CALL,
                strike,
                premium
            )

            # Epoch statistics
            self.epochs[-1].total_lp_profit += premium
            self.strike_values.append(value)
            self.strikes.append(strike)
            self.premiums.append(premium)

    def exercise_call_option(self, date: str, purchaser_id: int) -> None:
        if purchaser_id in self.options.keys():
            strike = self.options.pop(purchaser_id).strike
            end_eth_price = self.csv_processor.get_end_eth_price_wk(date)
            if strike <= end_eth_price:
                # Option is exercised
                self.total_usdt += strike
                self.total_underlying_asset_locked -= 1
                self.epochs[-1].total_lp_profit += strike
                self.epochs[-1].total_lp_profit -= end_eth_price

    def unlock_underlying_assets(self) -> None:
        self.total_underlying_asset_unlocked += self.total_underlying_asset_locked
        self.total_underlying_asset_locked = 0.0

    def convert_usdt_to_underlying_asset(self, date: str) -> None:
        self.total_underlying_asset_unlocked += self.total_usdt / \
            self.csv_processor.get_end_eth_price_wk(date)
        self.total_usdt = 0

    def calculate_lowest_strike(self, date: str) -> float:
        lowstrike = self.csv_processor.get_eth_price(date)
        lowstrike -= .5*lowstrike
        return lowstrike

    def calculate_highest_strike(self, date: str) -> float:
        highstrike = self.csv_processor.get_eth_price(date)
        highstrike += .5*highstrike
        return highstrike

    def calculate_strike_price(
        self,
        value: float,
        date: str,
    ) -> float:
        '''
        Given a value in the range [0, 1] where 0 is the lowest possible strike
        price and 1 is the highest possible strike price, return the
        corresponding strike price.
        '''

        lowest = self.calculate_lowest_strike(date)
        highest = self.calculate_highest_strike(date)
        return lowest + (highest - lowest) * value

    def calculate_premium(
        self,
        date: str,
        strike: float,
    ) -> float:
        '''
        Given a date and a strike price, calculate the price of the option
        premium in USDT based on values from the CSVs. Black-Scholes options
        premium prediction.

        S = spot price of asset
        K = strike price of option
        T = time in years
        r = risk free interest rate
        sigma = annualized vol (vix as a percentage)
        '''

        S = self.csv_processor.get_eth_price(date)
        K = strike
        T = 7.0 / 365.0
        r = self.csv_processor.get_r(date)
        sigma = self.csv_processor.get_vol(date)
        N = norm.cdf

        d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        premium = S * N(d1) - K * np.exp(-r*T) * N(d2)
        return premium

    def initialize_epoch_statistics(self, date: str) -> None:
        self.epochs.append(Epoch(
            date,
            self.csv_processor.get_end_eth_price_wk(date),
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
