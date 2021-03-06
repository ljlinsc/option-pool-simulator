from dataclasses import dataclass
from typing import List

import altair as alt
import numpy as np

from simulation.option_pool import OptionPool


@dataclass
class DataValue:
    distribution: str
    value: float


class DataProcessor:
    def get_data_by_epoch(option_pools: List[OptionPool]) -> alt.Data:
        return alt.Data(values=[dict(
            epoch.__dict__,
            purchaser_distribution=option_pool.purchaser_distribution.name
        ) for option_pool in option_pools for epoch in option_pool.epochs])

    def get_strike_values_data(option_pools: List[OptionPool]) -> alt.Data:
        data = []
        for option_pool in option_pools:
            option_pool_data = [
                {
                    'value': np.around(i, 2),
                    'frequency': 0,
                    'distribution': option_pool.purchaser_distribution.name
                }
                for i in np.arange(0.05, 1.05, 0.05)]
            for strike_value in option_pool.strike_values:
                for i in range(len(option_pool_data)):
                    if option_pool_data[i]['value'] >= strike_value:
                        option_pool_data[i]['frequency'] += 1
                        break
            data.extend(option_pool_data)
        return alt.Data(values=data)

    def get_total_lp_profit(option_pools: List[OptionPool]) -> List[DataValue]:
        data = []
        for option_pool in option_pools:
            option_pool_data = DataValue(
                option_pool.purchaser_distribution.name,
                0.0
            )
            for epoch in option_pool.epochs:
                option_pool_data.value += epoch.total_lp_profit
            data.append(option_pool_data)
        return data
