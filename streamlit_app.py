from datetime import datetime, timedelta

import altair as alt
import pandas as pd
import streamlit as st

from data_classes.distribution import Distribution, LPDistribution, PurchaserDistribution
from data_classes.underlying_asset import UnderlyingAsset
from simulation.simulation import Simulation
from utils.csv_processor import CSVProcessor
from utils.data_processor import DataProcessor
from utils.formatter import create_layered_bar_chart, get_dollar_str


# PAGE CONFIGURATION

st.set_page_config(
    page_title="Option Pool Simulator",
    layout="wide",
    initial_sidebar_state="expanded"
)
st.title("Option Pool Simulator")

# PARAMETERS

with st.sidebar:
    underlying_asset = st.selectbox(
        "Underlying asset",
        ["ETH", "TSLA"]
    )
    if underlying_asset == "ETH":
        csv_processor = CSVProcessor("data/eth.csv")
    elif underlying_asset == "TSLA":
        csv_processor = CSVProcessor("data/tsla.csv")

    start_date = st.date_input(
        "Start date",
        min_value=csv_processor.get_first_date(),
        max_value=csv_processor.get_last_date() - timedelta(days=7),
        value=csv_processor.get_first_date()
    )

    with st.form("input_parameters"):
        num_epochs = st.number_input(
            "Number of epochs",
            min_value=1,
            max_value=csv_processor.get_num_weeks_after_date(
                start_date)
        )
        num_purchasers = st.number_input(
            "Number of option purchasers",
            min_value=1,
            value=3
        )
        num_liquidity_providers = st.number_input(
            "Number of liquidity providers",
            min_value=1,
            value=3
        )
        purchaser_distribution_selections = st.multiselect(
            "Purchaser Distribution",
            [
                "Uniform",
                "Normal",
                "Skewed in the money",
                "Skewed out of the money",
                "Skewed extremely in the money",
                "Skewed extremely out of the money"
            ]
        )
        lp_distribution_selection = st.selectbox(
            "Liquidity Provider Distribution",
            ["Uniform", "Normal"]
        )

        submitted = st.form_submit_button("Run")

# RESULTS

tvl_container = st.empty()
option_pool_profit_container = st.empty()
lp_profit_container = st.empty()
underlying_price_container = st.empty()
purchaser_strike_value_container = st.empty()

if submitted:

    # SIMULATION

    epoch_dates = [
        datetime.combine(start_date + timedelta(7 * i), datetime.min.time())
        for i in range(num_epochs + 1)
    ]

    if underlying_asset == "ETH":
        asset = UnderlyingAsset.ETH
    elif underlying_asset == "TSLA":
        asset = UnderlyingAsset.TSLA

    purchaser_distributions = []
    if "Uniform" in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.UNIFORM)
    if "Normal" in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.NORMAL)
    if "Skewed in the money" in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.SKEWIN)
    if "Skewed out of the money" in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.SKEWOUT)
    if "Skewed extremely in the money" in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.EXTREMESKEWIN)
    if "Skewed extremely out of the money" in purchaser_distribution_selections:
        purchaser_distributions.append(PurchaserDistribution.EXTREMESKEWOUT)

    if lp_distribution_selection == "Uniform":
        lp_distribution = LPDistribution.UNIFORM
    elif lp_distribution_selection == "Normal":
        lp_distribution = LPDistribution.NORMAL

    simulations = [Simulation(
        csv_processor,
        num_liquidity_providers,
        num_purchasers,
        epoch_dates,
        Distribution(purchaser_distribution),
        Distribution(lp_distribution),
        asset
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
    underlying_price_container.empty()

    with tvl_container.container():
        st.subheader("Total value locked in the option pool")

        st.markdown("Every epoch, purchasers will attempt to purchase an option every epoch, and their options are automatically exercised depending on the end price of " +
                    underlying_asset + " at the end of the epoch.")

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

        st.altair_chart(create_layered_bar_chart(
            epoch_data,
            "start_date:O",
            "Epoch",
            "total_value_locked:Q",
            "Total value locked (USDT)",
            "purchaser_distribution:O",
            "Purchaser distribution"
        ), use_container_width=True)

    with option_pool_profit_container.container():
        st.subheader("Total option pool profit by epoch")

        st.altair_chart(create_layered_bar_chart(
            epoch_data,
            "start_date:O",
            "Epoch",
            "total_profit:Q",
            "Total profit (USDT)",
            "purchaser_distribution:O",
            "Purchaser distribution"
        ), use_container_width=True)

    with lp_profit_container.container():
        st.subheader("Liquidity provider profit by epoch")

        st.markdown("At the beginning of each epoch, LP profit is incremented by the summation of all premiums paid by purchasers. At the end of the epoch, purchasers will exercise their options if the price of " +
                    underlying_asset + " is greater than the strike price. When an option is exercised, the LP profit is incremented by the corresponding strike price and decremented by the price of " + underlying_asset + ".")

        st.latex(r"""
            \text{LP profit over an epoch} = \sum_{\text{purchased options}} \text{premium} + \sum_{\text{exercised options}} \left(\text{strike} - \text{price of the underlying asset in USD}\right)
        """)

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

        st.altair_chart(create_layered_bar_chart(
            epoch_data,
            "start_date:O",
            "Epoch",
            "total_lp_profit:Q",
            "Total liquidity provider profit (USDT)",
            "purchaser_distribution:O",
            "Purchaser distribution"
        ), use_container_width=True)

    with underlying_price_container.container():
        st.subheader("Price of " + underlying_asset)

        st.altair_chart(alt.Chart(epoch_data).mark_line(
            color="gray"
        ).encode(
            x=alt.X("start_date:O", axis=alt.Axis(title="Epoch")),
            y=alt.Y("end_underlying_price:Q", axis=alt.Axis(format="$.2f",
                    title="USDT"))
        ), use_container_width=True)

    with purchaser_strike_value_container.container():
        st.subheader("Purchaser strike price selection distribution")

        st.altair_chart(alt.Chart(strike_values_data).mark_bar().encode(
            x=alt.X("value:O", axis=alt.Axis(title="Value")),
            y=alt.Y("frequency:Q", axis=alt.Axis(title="Frequency")),
            color=alt.value("black")
        ), use_container_width=True)
