import requests
import streamlit as st

def get_company_data(ticker):
    api_key = st.secrets["FMP_API_KEY"]
    base_url = "https://financialmodelingprep.com/api/v3"

    cf_url = f"{base_url}/cash-flow-statement/{ticker}?limit=1&apikey={api_key}"
    cf_data = requests.get(cf_url).json()

    profile_url = f"{base_url}/profile/{ticker}?apikey={api_key}"
    profile_data = requests.get(profile_url).json()

    bs_url = f"{base_url}/balance-sheet-statement/{ticker}?limit=1&apikey={api_key}"
    bs_data = requests.get(bs_url).json()

    # TEMPORARY DEBUG: show us exactly what each API call returned
    st.write("Cash flow response:", cf_data)
    st.write("Profile response:", profile_data)
    st.write("Balance sheet response:", bs_data)

    return None
