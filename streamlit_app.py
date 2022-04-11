import altair as alt
import json
import numpy as np
import pandas as pd
import streamlit as st

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
    size_of_pool = st.number_input(
        'Size in Dollars',
        min_value=1,
        value=100000
    )
    start_week = st.selectbox(
        'Start week',
        dates
    )
    end_week = st.selectbox(
        'End week',
        dates
    )
    submitted = st.form_submit_button('Run')

if submitted:

    # SIMULATION

    epoch_dates = dates[dates.index(start_week):dates.index(end_week) + 1]

    sim = Simulation(
        num_liquidity_providers,
        num_purchasers,
        epoch_dates,
        size_of_pool
    )
    option_pool = sim.run()

    csv_processor = CSVProcessor()
    data_processor = DataProcessor(epoch_dates, option_pool, size_of_pool)
    data_by_epoch = alt.Data(
        values=[epoch.__dict__ for epoch in data_processor.getEpochs()])

    # OUTPUT

    st.header('Simulation Results')

    # with st.container():
    #     st.subheader('Profit of LPs: ' + '${:.2f}'.format(csv_processor.calc_profit(size_of_pool)))

    with st.container():
        st.subheader('Total value locked in the option pool')

        st.altair_chart(alt.Chart(data_by_epoch).mark_area(
            color="lightblue",
            interpolate='step-after',
            line=True
        ).encode(
            x=alt.X('start_date:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('total_value_locked:Q', axis=alt.Axis(format='$.2f',
                    title='Total value locked in the option pool (USD)'))
        ), use_container_width=True)
