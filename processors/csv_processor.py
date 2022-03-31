import pandas as pd
from numpy import around
from random import randint
from collections import Counter

class CSVProcessor:
    def __init__(self, size_of_pool: float) -> None:
        self.size_of_pool = size_of_pool
    
    def calc_profit(self, size_of_pool: float) -> float:
        chain = pd.read_csv("data/chaincsv1.csv")
        sizecounter = 0
        totallpprofit = 0
        collateralcounter = 0
        totalbuyerprofit = 0

        maxprice = chain.iloc[0]['sprice']
        strikes = []

        while(sizecounter + maxprice < size_of_pool):
            rint = randint(0,58)
            strikes.append(chain.iloc[rint]['strike'])
            totallpprofit += chain.iloc[rint]['trueprofit']
            sizecounter += chain.iloc[rint]['sprice']
            collateralcounter += chain.iloc[rint]['spot']
            totalbuyerprofit += chain.iloc[rint]['buyerprofit']
        
        totallpprofit = around((totallpprofit*100)/100)
        return totallpprofit