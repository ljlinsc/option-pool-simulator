import pandas as pd
from numpy import around
from random import randint
from collections import Counter
from typing import List


class CSVProcessor:
    def calc_profit(self, size_of_pool: float) -> float:
        chain = pd.read_csv("data/chaincsv1weeklychainst20200418.csv")
        sizecounter = 0
        totallpprofit = 0
        collateralcounter = 0
        totalbuyerprofit = 0

        maxprice = chain.iloc[0]['soptprice']
        strikes = []

        while(sizecounter + maxprice < size_of_pool):
            rint = randint(0, 58)
            strikes.append(chain.iloc[rint]['strike'])
            totallpprofit += chain.iloc[rint]['truelpprofit']
            sizecounter += chain.iloc[rint]['soptprice']
            collateralcounter += chain.iloc[rint]['spot']
            totalbuyerprofit += chain.iloc[rint]['buyerprofit']

        totallpprofit = around((totallpprofit*100)/100)
        return totallpprofit

    def get_weekly_chain(self, date: str) -> pd.DataFrame:
        return pd.read_csv('data/chaincsv1weeklychainst' + date.replace('-', '') + '.csv')

    def get_weekly_chain_property(self, date: str, option_index: int, property: str) -> float:
        return self.get_weekly_chain(date).iloc[option_index][property]

    def get_strike_price(self, date: str, option_index: int) -> float:
        print(date)
        return self.get_weekly_chain_property(date, option_index, 'strike')

    def get_premium(self, date: str, option_index: int) -> float:
        return self.get_weekly_chain_property(date, option_index, 'soptprice')

    def get_end_eth_price(self, date: str) -> float:
        return self.get_weekly_chain_property(date, 0, 'endethprice')        
