import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

from simulation import Simulation

# PAGE CONFIGURATION

st.set_page_config(
    page_title='Option Pool Simulator',
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title('Option Pool Simulator')

# PARAMETERS

with st.sidebar.form('input_parameters'):
    num_option_buyers = st.number_input(
        'Number of option buyers',
        min_value=1,
        value=3
    )
    num_liquidity_providers = st.number_input(
        'Number of liquidity providers',
        min_value=1,
        value=3
    )
    underlying_asset = st.selectbox(
        'Underlying asset',
        ('ETH', 'USD')
    )
    option_type = st.radio(
        'Type of option',
        ('Call option', 'Put option')
    )
    num_epochs = st.number_input(
        'Number of epochs',
        min_value=1,
        value=10
    )
    epoch_type = st.radio(
        'Type of epoch',
        ('Week', 'Month')
    )
    submitted = st.form_submit_button('Run')

# SIMULATION

if submitted:
    data = alt.Data(values=Simulation().getData())

    # OUTPUT

    st.header('Simulation Results')

    with st.container():
        st.subheader('Total collateral in the option pool')

        st.altair_chart(alt.Chart(data).mark_area(
            color="lightblue",
            interpolate='step-after',
            line=True
        ).encode(
            x=alt.X('epoch:O', axis=alt.Axis(title='Epoch')),
            y=alt.Y('collateral:Q', axis=alt.Axis(format='$.2f', title='Total collateral in the option pool (USD)'))
        ))
