# Option Pool Simulator

## Table of Contents

1. [Introduction](#introduction)
2. [Development](#development)
    1. [Using GitHub](#using-github)
    2. [Setting Up Your Local Environment](#setting-up-your-local-environment)
    3. [Developing In Your Local Environment](#developing-in-your-local-environment)

## Introduction

This program simulates simplified option pools. [Option pools](https://docs.dopex.io/pools) are an upcoming feature in the [Dopex protocol](https://www.dopex.io/) where option buyers can purchase any amount of options at any strike price. Liquidity providers fund these pools in exchange for fees. The option buyers' earnings and the LPs' yields depend on the underlying asset's exercise price at the end of the epoch.

## Development

### Using GitHub

#### Setting up GitHub
1. Install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git)
2. Using your Command Prompt or Terminal, navigate into the folder you want this repository to live
3. Run `git clone https://github.com/ljlinsc/option-pool-simulator.git`
     1. If you are prompted to enter your GitHub username and password, do the following:
     2. In your web browser, go to https://github.com/settings/tokens
         1. Click "Generate new token"
         2. Fill in the "Note" text input - it can be anything (example: "My Windows Laptop")
         3. Change the "Expiration" to "No expiration"
         4. Check all of the boxes under "Select scopes"
         5. Copy the personal access token before it disappears
     3. Back in your Command Prompt or Terminal, enter your credientials:
         1. Username: Your GitHub username (example: ljlinsc)
         2. Password: The personal access token you just generated

#### Updating your Local Repository
Run `git pull` (make sure to do this frequently)

#### Pushing your Local Changes to GitHub
1. Save all of your files
2. Run `git status` and check that all of your changed files are listed
3. Run `git add .` (the `.` is not a typo!)
4. Run `git commit -m "short description of what you did"` (example: `git commit -m "Add weekly chain data"`)
5. Run `git push`

### Setting Up Your Local Environment

1. Install [Python](https://www.python.org/downloads/) 3.7 - 3.9
2. Run `pip install -r requirements.txt`

### Developing In Your Local Environment

1. Run `python -m streamlit run streamlit_app.py`
2. The Streamlit app will appear in a new tab in your web browser (your first run might take a while)
