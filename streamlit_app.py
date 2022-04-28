import altair as alt
import pandas as pd
import streamlit as st
from data_classes.distribution import Distribution, LPDistribution, PurchaserDistribution

from processors.csv_processor import CSVProcessor
from processors.txt_processor import TXTProcessor
from simulation.simulation import Simulation
from processors.data_processor import DataProcessor

csv_processor = CSVProcessor()
txt_processor = TXTProcessor()
dates = txt_processor.getDates()


def get_dollar_str(value: float) -> str:
    if value < 0:
        dollar_str = "-"
    else:
        dollar_str = ""
    dollar_str += "$%.2f" % (value.__abs__())
    return dollar_str


# PAGE CONFIGURATION

st.set_page_config(
    page_title='Option Pool Simulator',
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title('Option Pool Simulator')

# PARAMETERS

with st.sidebar.form('input_parameters'):
    num_purchasers = st.number_input(
        'Number of option purchasers',
        min_value=1,
        value=3
    )
    num_liquidity_providers = st.number_input(
        'Number of liquidity providers',
        min_value=1,
        value=3
    )
    start_week = st.selectbox(
        'Start week',
        dates
    )
    end_week = st.selectbox(
        'End week',
        dates
    )
    purchaser_distribution_selections = st.multiselect(
        'Purchaser Distribution',
        ['Uniform',
        'Normal',
        'Skewed in the money',
        'Skewed out of the money',
        'Skewed extremely in the money',
        'Skewed extremely out of the money']
    )
    lp_distribution_selection = st.selectbox(
        'Liquidity Provider Distribution',
        ['Uniform', 'Normal']
    )
    submitted = st.form_submit_button('Run')

# RESULTS

tvl_container = st.empty()
option_pool_profit_container = st.empty()
lp_profit_container = st.empty()
eth_price_container = st.empty()
purchaser_strike_value_container = st.empty()

if submitted:

    epoch_dates = dates[dates.index(start_week):dates.index(end_week) + 1]

    # purchaser distribution setting
    purchaser_distributions = []
    if 'Uniform' in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.UNIFORM)
    if 'Normal' in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.NORMAL)
    if 'Skewed in the money' in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.SKEWIN)
    if 'Skewed out of the money' in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.SKEWOUT)
    if 'Skewed extremely in the money' in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.EXTREMESKEWIN)
    if 'Skewed extremely out of the money' in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.EXTREMESKEWOUT)

    # lp distribution selection
    if lp_distribution_selection == 'Uniform':
        lp_distribution = LPDistribution.UNIFORM
    elif lp_distribution_selection == 'Normal':
        lp_distribution = LPDistribution.NORMAL

    # SIMULATION

    simulations = [Simulation(
        csv_processor,
        num_liquidity_providers,
        num_purchasers,
        epoch_dates,
        Distribution(purchaser_distribution),
        Distribution(lp_distribution)
    ) for purchaser_distribution in purchaser_distributions]
    option_pools = [simulation.run() for simulation in simulations]
    epoch_data = DataProcessor.get_data_by_epoch(option_pools)
    strike_values_data = DataProcessor.get_strike_values_data(option_pools)
    total_lp_profit_data = DataProcessor.get_total_lp_profit(option_pools)

    # OUTPUT

    # Ensures that the graphs re-render with the new data
    tvl_container.empty()
    option_pool_profit_container.empty()
    purchaser_strike_value_container.empty()
    lp_profit_container.empty()
    eth_price_container.empty()

    with tvl_container.container():
        st.subheader('Total value locked in the option pool')

        st.markdown("Every epoch, LPs deposit 1-3 ETH and attempt to withdraw up to 2 ETH. Purchasers will attempt to purchase an option every epoch, and their options are automatically exercised depending on the end price of ETH at the end of the epoch.")

        st.table(pd.DataFrame(
            [[
                option_pool.purchaser_distribution.name,
                get_dollar_str(option_pool.epochs[-1].total_value_locked)
            ] for option_pool in option_pools],
            columns=(
                "Purchaser distribution",
                "Final TVL of the option pool"
            ),
        ))

        st.altair_chart(alt.Chart(epoch_data).mark_bar(opacity=0.7).encode(
            x=alt.X(
                'start_date:O',
                axis=alt.Axis(title='Epoch')
            ),
            y=alt.Y(
                'total_value_locked:Q',
                axis=alt.Axis(
                    format='$.2f', title='Total value locked (USDT)'),
                stack=None
            ),
            color=alt.Color(
                'purchaser_distribution:O',
                scale=alt.Scale(scheme='set1'),
                title='Purchaser distribution'
            )
        ), use_container_width=True)

    with option_pool_profit_container.container():
        st.subheader('Total option pool profit by epoch')

        st.altair_chart(alt.Chart(epoch_data).mark_bar(opacity=0.7).encode(
            x=alt.X(
                'start_date:O',
                axis=alt.Axis(title='Epoch')
            ),
            y=alt.Y(
                'total_profit:Q',
                axis=alt.Axis(format='$.2f', title='Total profit (USDT)'),
                stack=None
            ),
            color=alt.Color(
                'purchaser_distribution:O',
                scale=alt.Scale(scheme='set1'),
                title='Purchaser distribution'
            )
        ), use_container_width=True)

    with lp_profit_container.container():
        st.subheader('Liquidity provider profit by epoch')

        st.markdown("At the beginning of each epoch, LP profit is incremented by the summation of all premiums paid by purchasers. At the end of the epoch, purchasers will exercise their options if the price of ETH is greater than the strike price. When an option is exercised, the LP profit is incremented by the corresponding strike price and decremented by the price of ETH.")

        st.latex(r'''
            \text{LP profit over an epoch} = \sum_{\text{purchased options}} \text{premium} + \sum_{\text{exercised options}} \left(\text{strike} - \text{price of ETH in USD}\right)
        ''')

        st.table(pd.DataFrame(
            [[
                data.distribution,
                get_dollar_str(data.value)
            ] for data in total_lp_profit_data],
            columns=("Purchaser distribution", "Total LP profit"),
        ))

        if len(total_lp_profit_data) > 1:
            most_profitable = total_lp_profit_data[0]
            for i in range(1, len(total_lp_profit_data)):
                if total_lp_profit_data[i].value > most_profitable.value:
                    most_profitable = total_lp_profit_data[i]
            st.markdown(
                "LPs will profit most when purchaser strikes are **" +
                most_profitable.distribution.lower() + "**."
            )

        if len(total_lp_profit_data) > 1:
            least_profitable = total_lp_profit_data[0]
            for i in range(1, len(total_lp_profit_data)):
                if total_lp_profit_data[i].value < least_profitable.value:
                    least_profitable = total_lp_profit_data[i]
            st.markdown(
                "LPs will profit least when purchaser strikes are **" +
                least_profitable.distribution.lower() + "**."
            )

        st.altair_chart(alt.Chart(epoch_data).mark_bar(opacity=0.7).encode(
            x=alt.X(
                'start_date:O',
                axis=alt.Axis(title='Epoch')
            ),
            y=alt.Y(
                'total_lp_profit:Q',
                axis=alt.Axis(
                    format='$.2f', title='Total liquidity provider profit (USDT)'),
                stack=None
            ),
            color=alt.Color(
                'purchaser_distribution:O',
                scale=alt.Scale(scheme='set1'),
                title='Purchaser distribution'
            )
        ), use_container_width=True)

    with eth_price_container.container():
        st.subheader('Price of ETH')

        st.altair_chart(alt.Chart(epoch_data).mark_line(
            color="gray"
        ).encode(
            x=alt.X('start_date:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('end_eth_price:Q', axis=alt.Axis(format='$.2f',
                    title='USDT'))
        ), use_container_width=True)

    with purchaser_strike_value_container.container():
        st.subheader('Purchaser strike price selection distribution')

        st.altair_chart(alt.Chart(strike_values_data).mark_bar().encode(
            x=alt.X('value:O', axis=alt.Axis(title='Value')),
            y=alt.Y('frequency:Q', axis=alt.Axis(title='Frequency')),
            color=alt.value("black")
        ), use_container_width=True)
