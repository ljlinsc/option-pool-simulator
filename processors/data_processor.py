from typing import List
import altair as alt
import numpy as np

from simulation.option_pool import OptionPool


class DataProcessor:
    def get_data_by_epoch(option_pools: List[OptionPool]) -> alt.Data:
        return alt.Data(values=[dict(
            epoch.__dict__,
            purchaser_distribution=option_pool.purchaser_distribution.name
        ) for option_pool in option_pools for epoch in option_pool.epochs])

    def get_strike_values_data(option_pools: List[OptionPool]) -> alt.Data:
        data = [{'value': np.around(i, 2), 'frequency': 0}
                for i in np.arange(0.05, 1.05, 0.05)]
        for option_pool in option_pools:
            for strike_value in option_pool.strike_values:
                for i in range(len(data)):
                    if data[i]['value'] >= strike_value:
                        data[i]['frequency'] += 1
                        break
        return alt.Data(values=data)
