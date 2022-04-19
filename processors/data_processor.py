import altair as alt
import numpy as np

from simulation.option_pool import OptionPool


class DataProcessor:
    def get_strike_values_data(option_pool: OptionPool) -> alt.Data:
        data = [{'value': np.around(i, 2), 'frequency': 0}
                for i in np.arange(0.05, 1.05, 0.05)]
        for strike_value in option_pool.strike_values:
            for i in range(len(data)):
                if data[i]['value'] >= strike_value:
                    data[i]['frequency'] += 1
                    break
        return alt.Data(values=data)
