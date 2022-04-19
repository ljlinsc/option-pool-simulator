from datetime import timedelta
import pandas as pd


class CSVProcessor:
    def __init__(self) -> None:
        self.data = pd.read_csv(
            "data/optdata.csv", index_col='Date', parse_dates=['Date'])

    def get_eth_price(self, date: str) -> float:
        date = pd.to_datetime(date)
        return self.data.loc[date][2]

    def get_vol(self, date: str) -> float:
        date = pd.to_datetime(date)
        return self.data.loc[date][1]

    def get_r(self, date: str) -> float:
        date = pd.to_datetime(date)
        return self.data.loc[date][0]

    def get_end_eth_price_wk(self, date: str) -> float:
        date = pd.to_datetime(date)
        enddate = date + timedelta(days=7)
        return self.data.loc[enddate][2]
