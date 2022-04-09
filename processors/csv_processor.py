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
            rint = randint(0,58)
            strikes.append(chain.iloc[rint]['strike'])
            totallpprofit += chain.iloc[rint]['truelpprofit']
            sizecounter += chain.iloc[rint]['soptprice']
            collateralcounter += chain.iloc[rint]['spot']
            totalbuyerprofit += chain.iloc[rint]['buyerprofit']
        
        totallpprofit = around((totallpprofit*100)/100)
        return totallpprofit
    
    def get_strike_prices(self, date: str) -> List[float]:
        chain = pd.read_csv('data/chaincsv1weeklychainst' + date.replace('-', '') + '.csv')
        strike_prices = [chain.iloc[i]['strike'] for i in range(58)]
        return strike_prices

    def get_premium_prices(self, date: str) -> List[float]:
        chain = pd.read_csv('data/chaincsv1weeklychainst' + date.replace('-', '') + '.csv')
        premium_prices = [chain.iloc[i]['soptprice'] for i in range(58)]
        return premium_prices

    def get_end_underlying_asset_price(self, date: str) -> float:
        chain = pd.read_csv('data/chaincsv1weeklychainst' + date.replace('-', '') + '.csv')
        return chain.iloc[0]['endethprice']
