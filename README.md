# Option Pool Simulator

## Table of Contents

1. [Introduction](#introduction)
2. [Development](#development)
    1. [Setting Up Your Local Environment](#setting-up-your-local-environment)
    2. [Developing In Your Local Environment](#developing-in-your-local-environment)

## Introduction

This program simulates simplified option pools. [Option pools](https://docs.dopex.io/pools) are an upcoming feature in the [Dopex protocol](https://www.dopex.io/) where option buyers can purchase any amount of options at any strike price. Liquidity providers fund these pools in exchange for fees. The option buyers' earnings and the LPs' yields depend on the underlying asset's exercise price at the end of the epoch.

## Development

### Setting Up Your Local Environment

1. Install [Python](https://www.python.org/downloads/) 3.7 - 3.9
2. Run `pip install -r requirements.txt`

### Developing In Your Local Environment

1. Run `python -m streamlit run streamlit_app.py`
2. The Streamlit app will appear in a new tab in your web browser (your first run might take a while)