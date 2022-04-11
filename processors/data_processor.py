from data_classes.epoch import Epoch
from typing import List

from simulation.option_pool import OptionPool


class DataProcessor:
    def __init__(self, epoch_dates: List[str], option_pool: OptionPool, size_of_pool: int) -> None:
        self.epoch_dates = epoch_dates
        self.option_pool = option_pool
        self.size_of_pool = size_of_pool

    def getEpochs(self) -> List[Epoch]:
        epochs: List[Epoch] = [Epoch(date, 0.0, 0.0)
                               for date in self.epoch_dates]

        # Total value locked (USDT) at the end of each epoch
        for i in range(len(epochs)):
            epochs[i].total_value_locked = self.option_pool.end_of_epoch_tvls[i]

        # Total profit (USDT) for each epoch
        epochs[0].total_profit = epochs[0].total_value_locked
        for i in range(1, len(epochs)):
            epochs[i].total_profit = epochs[i].total_value_locked - \
                epochs[i - 1].total_value_locked

        return epochs
