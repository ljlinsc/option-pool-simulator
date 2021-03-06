from datetime import datetime

import numpy as np
from scipy.stats import norm

from data_classes.distribution import Distribution
from data_classes.epoch import Epoch
from data_classes.option import Option, OptionType
from data_classes.underlying_asset import UnderlyingAsset
from utils.csv_processor import CSVProcessor


class OptionPool:
    def __init__(
        self,
        csv_processor: CSVProcessor,
        purchaser_distribution: Distribution
    ) -> None:
        self.csv_processor = csv_processor
        self.purchaser_distribution = purchaser_distribution
        self.total_underlying_asset_unlocked = 0.0
        self.total_underlying_asset_locked = 0.0
        self.total_usdt = 0.0
        self.options = dict()

        # Statistics
        self.epochs = []
        self.strike_values = []
        self.strikes = []
        self.premiums = []

    def deposit(self, value: float, asset: UnderlyingAsset) -> None:
        if asset == UnderlyingAsset.USDT:
            self.total_usdt += value
        else:
            self.total_underlying_asset_unlocked += value

    def withdraw(self, value: float, asset: UnderlyingAsset) -> bool:
        if asset == UnderlyingAsset.USDT:
            if self.total_usdt >= value:
                self.total_usdt -= value
                return True
        else:
            if self.total_underlying_asset_unlocked >= value:
                self.total_underlying_asset_unlocked -= value
                return True
        return False

    def purchase_call_option(
        self,
        date: datetime,
        purchaser_id: int,
        value: float
    ) -> float:
        """Returns the premium required to purchase a call option on 1 of the
        underlying assets stored in the option pool. Otherwise, returns -1 to
        indicate that there are no unlocked assets available in the pool.
        """
        if self.total_underlying_asset_unlocked > 0:
            strike = self.calculate_strike_price(value, date)
            premium = self.calculate_premium(date, strike)

            # Lock the underlying asset
            self.total_underlying_asset_unlocked -= 1
            self.total_underlying_asset_locked += 1

            # Increment the pool's USDT by the premium (indicating that the
            # purchaser paid this amount)
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

            return premium
        return -1

    def exercise_call_option(self, date: datetime, purchaser_id: int) -> float:
        """Exercises the call option and returns the strike price. Otherwise,
        returns -1 if the call option was not exercised or the call option was
        not found.
        """
        if purchaser_id in self.options.keys():
            strike = self.options.pop(purchaser_id).strike
            end_underlying_price = self.csv_processor.get_underlying_price(
                date)
            if strike <= end_underlying_price:
                # Option is exercised
                self.total_usdt += strike
                self.total_underlying_asset_locked -= 1
                self.epochs[-1].total_lp_profit += strike
                self.epochs[-1].total_lp_profit -= end_underlying_price

                return strike
        return -1

    def unlock_underlying_assets(self) -> None:
        self.total_underlying_asset_unlocked += self.total_underlying_asset_locked
        self.total_underlying_asset_locked = 0.0

    def convert_usdt_to_underlying_asset(self, date: datetime) -> None:
        self.total_underlying_asset_unlocked += self.total_usdt / \
            self.csv_processor.get_underlying_price(date)
        self.total_usdt = 0

    def calculate_lowest_strike(self, date: datetime) -> float:
        lowstrike = self.csv_processor.get_underlying_price(date)
        lowstrike -= .5*lowstrike
        return lowstrike

    def calculate_highest_strike(self, date: datetime) -> float:
        highstrike = self.csv_processor.get_underlying_price(date)
        highstrike += .5*highstrike
        return highstrike

    def calculate_strike_price(
        self,
        value: float,
        date: datetime,
    ) -> float:
        """Returns a strike price depending on the lowest permitted strike
        price, the highest permitted strike price, and a value [0, 1] indicating
        a random strike price within that range.
        """
        lowest = self.calculate_lowest_strike(date)
        highest = self.calculate_highest_strike(date)
        return lowest + (highest - lowest) * value

    def calculate_premium(
        self,
        date: datetime,
        strike: float,
    ) -> float:
        """Calculates the premium in USDT using Black-Scholes options premium
        prediction based on the date and strike price.

        S = spot price of asset
        K = strike price of option
        T = time in years
        r = risk free interest rate
        sigma = annualized vol (vix as a percentage)
        """
        S = self.csv_processor.get_underlying_price(date)
        K = strike
        T = 7.0 / 365.0
        r = self.csv_processor.get_r(date)
        sigma = self.csv_processor.get_vol(date)
        N = norm.cdf

        d1 = (np.log(S/K) + (r + sigma**2/2)*T) / (sigma*np.sqrt(T))
        d2 = d1 - sigma * np.sqrt(T)
        premium = S * N(d1) - K * np.exp(-r*T) * N(d2)
        return premium

    def initialize_epoch_statistics(self, date: datetime) -> None:
        self.epochs.append(Epoch(
            str(date.date()),
            self.csv_processor.get_underlying_price(date),
            0.0,
            0.0,
            0.0
        ))

    def calculate_epoch_statistics(self) -> None:
        # Calculate the total value locked in the option pool (USDT)
        self.epochs[-1].total_value_locked = self.epochs[-1].end_underlying_price * \
            self.total_underlying_asset_unlocked

        # Calculate the total profit of the option pool (USDT)
        if len(self.epochs) == 1:
            self.epochs[-1].total_profit = self.epochs[-1].total_value_locked
        else:
            self.epochs[-1].total_profit = self.epochs[-1].total_value_locked - \
                self.epochs[-2].total_value_locked
