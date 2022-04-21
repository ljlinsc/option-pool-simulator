import altair as alt
import streamlit as st
from data_classes.distribution import Distribution, LPDistribution, PurchaserDistribution

from processors.csv_processor import CSVProcessor
from processors.txt_processor import TXTProcessor
from simulation.simulation import Simulation
from processors.data_processor import DataProcessor

csv_processor = CSVProcessor()
txt_processor = TXTProcessor()
dates = txt_processor.getDates()

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
    purchaser_distribution_selection = st.selectbox(
        'Purchaser Distribution',
        ['Uniform', 'Normal', 'Skew in the money', 'Skew out the money']
    )
    lp_distribution_selection = st.selectbox(
        'Liquidity Provider Distribution',
        ['Uniform']
    )
    submitted = st.form_submit_button('Run')

# RESULTS

st.header('Simulation Results')

tvl_container = st.empty()
option_pool_profit_container = st.empty()
purchaser_strike_value_container = st.empty()
lp_profit_container = st.empty()
eth_price_container = st.empty()

if submitted:

    epoch_dates = dates[dates.index(start_week):dates.index(end_week) + 1]

    # purchaser distribution setting
    if purchaser_distribution_selection == 'Uniform':
        purchaser_distribution = PurchaserDistribution.UNIFORM
    elif purchaser_distribution_selection == 'Normal':
        purchaser_distribution = PurchaserDistribution.NORMAL
    elif purchaser_distribution_selection == 'Skew in the money':
        purchaser_distribution = PurchaserDistribution.SKEWIN
    elif purchaser_distribution_selection == 'Skew out the money':
        purchaser_distribution = PurchaserDistribution.SKEWOUT

    # lp distribution selection
    if lp_distribution_selection == 'Uniform':
        lp_distribution = LPDistribution.UNIFORM

    # SIMULATION

    sim = Simulation(
        csv_processor,
        num_liquidity_providers,
        num_purchasers,
        epoch_dates,
        Distribution(purchaser_distribution, lp_distribution)
    )
    option_pool = sim.run()

    data_by_epoch = alt.Data(
        values=[epoch.__dict__ for epoch in option_pool.epochs])
    strike_value_data = DataProcessor.get_strike_values_data(option_pool)

    # OUTPUT

    # Ensures that the graphs re-render with the new data
    tvl_container.empty()
    option_pool_profit_container.empty()
    purchaser_strike_value_container.empty()
    lp_profit_container.empty()
    eth_price_container.empty()

    with tvl_container.container():
        st.subheader('Total value locked in the option pool')

        st.altair_chart(alt.Chart(data_by_epoch).mark_bar().encode(
            x=alt.X('start_date:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('total_value_locked:Q', axis=alt.Axis(format='$.2f',
                    title='Total value locked (USDT)')),
            color=alt.condition(
                alt.datum.total_value_locked > 0,
                alt.value("green"),
                alt.value("red")
            )
        ), use_container_width=True)

    with option_pool_profit_container.container():
        st.subheader('Total option pool profit by epoch')

        st.altair_chart(alt.Chart(data_by_epoch).mark_bar().encode(
            x=alt.X('start_date:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('total_profit:Q', axis=alt.Axis(format='$.2f',
                    title='Total profit (USDT)')),
            color=alt.condition(
                alt.datum.total_profit > 0,
                alt.value("green"),
                alt.value("red")
            )
        ), use_container_width=True)

    with purchaser_strike_value_container.container():
        st.subheader('Purchaser strike price selection distribution')

        st.altair_chart(alt.Chart(strike_value_data).mark_bar().encode(
            x=alt.X('value:O', axis=alt.Axis(title='Value')),
            y=alt.Y('frequency:Q', axis=alt.Axis(title='Frequency')),
            color=alt.value("blue")
        ), use_container_width=True)

    with lp_profit_container.container():
        st.subheader('Total liquidity provider profit by epoch')

        st.altair_chart(alt.Chart(data_by_epoch).mark_bar().encode(
            x=alt.X('start_date:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('total_lp_profit:Q', axis=alt.Axis(format='$.2f',
                    title='Total liquidity provider profit (USDT)')),
            color=alt.condition(
                alt.datum.total_lp_profit > 0,
                alt.value("green"),
                alt.value("red")
            )
        ), use_container_width=True)

    with eth_price_container.container():
        st.subheader('Price of ETH')

        st.altair_chart(alt.Chart(data_by_epoch).mark_line(
            color="gray"
        ).encode(
            x=alt.X('start_date:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('end_eth_price:Q', axis=alt.Axis(format='$.2f',
                    title='USDT'))
        ), use_container_width=True)
