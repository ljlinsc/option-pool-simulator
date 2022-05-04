from datetime import date, datetime
from math import floor
import pandas as pd


class CSVProcessor:
    def __init__(self, file_name: str) -> None:
        self.data = pd.read_csv(
            file_name,
            index_col='Date',
            parse_dates=['Date']
        )

    def get_underlying_price(self, date: datetime) -> float:
        return self.data.loc[date][2]

    def get_vol(self, date: datetime) -> float:
        return self.data.loc[date][1]

    def get_r(self, date: datetime) -> float:
        return self.data.loc[date][0]

    def get_first_date(self) -> datetime:
        return self.data.index[0]

    def get_last_date(self) -> datetime:
        return self.data.index[-1]

    def get_num_weeks_after_date(self, date: date) -> int:
        return floor((self.get_last_date().date() - date).days / 7)
