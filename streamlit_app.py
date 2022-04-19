import altair as alt
import streamlit as st
from data_classes.distribution import Distribution, PurchaserDist

from processors.csv_processor import CSVProcessor
from processors.txt_processor import TXTProcessor
from simulation.simulation import Simulation
from processors.data_processor import DataProcessor

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
    purchaser_dist_selection = st.selectbox(
        'Purchaser Distribution',
        ['Uniform', 'Normal', 'Skew in the money', 'Skew out the money', 'poop']
    )
    lp_dist_selection = st.selectbox(
        'Liquidity Provider Distribution',
        ['Uniform']
    )
    submitted = st.form_submit_button('Run')

if submitted:

    # SIMULATION

    epoch_dates = dates[dates.index(start_week):dates.index(end_week) + 1]

    # purchaser distribution setting
    if purchaser_dist_selection == 'Normal':
        pdist = PurchaserDist.NORMAL
    elif purchaser_dist_selection == 'Skew in the money':
        pdist = PurchaserDist.SKEWIN
    elif purchaser_dist_selection == 'Skew out the money':
        pdist = PurchaserDist.SKEWOUT
    else:
        pdist = PurchaserDist.UNIFORM

    # lp distribution selection
    if lp_dist_selection == 'Uniform':
        lpdist = LPDist.UNIFORM
    else:
        lpdist = LPDist.UNIFORM


    sim = Simulation(
        num_liquidity_providers,
        num_purchasers,
        epoch_dates,
        Distribution(pdist, lpdist)
    )
    option_pool = sim.run()

    csv_processor = CSVProcessor()
    data_processor = DataProcessor(epoch_dates, option_pool)
    data_by_epoch = alt.Data(
        values=[epoch.__dict__ for epoch in option_pool.epochs])

    # OUTPUT

    st.header('Simulation Results')

    with st.container():
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

    with st.container():
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

    with st.container():
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

    with st.container():
        st.subheader('Price of ETH')

        st.altair_chart(alt.Chart(data_by_epoch).mark_line(
            color="gray"
        ).encode(
            x=alt.X('start_date:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('end_eth_price:Q', axis=alt.Axis(format='$.2f',
                    title='USDT'))
        ), use_container_width=True)
