import requests
import streamlit as st

def get_company_data(ticker):
    """
    Pulls key financial data for a company from Financial Modeling Prep.
    Returns a dictionary of the numbers we need for the DCF, or None if
    the ticker is invalid / data is missing.
    """
    api_key = st.secrets["FMP_API_KEY"]
    base_url = "https://financialmodelingprep.com/api/v3"

    try:
        # Get latest free cash flow figures
        cf_url = f"{base_url}/cash-flow-statement/{ticker}?limit=1&apikey={api_key}"
        cf_data = requests.get(cf_url).json()

        # Get current share price and shares outstanding
        profile_url = f"{base_url}/profile/{ticker}?apikey={api_key}"
        profile_data = requests.get(profile_url).json()

        # Get balance sheet for net debt
        bs_url = f"{base_url}/balance-sheet-statement/{ticker}?limit=1&apikey={api_key}"
        bs_data = requests.get(bs_url).json()

        if not cf_data or not profile_data or not bs_data:
            return None

        cf = cf_data[0]
        profile = profile_data[0]
        bs = bs_data[0]

        free_cash_flow = cf.get("freeCashFlow", 0)
        current_price = profile.get("price", 0)
        shares_outstanding = profile.get("mktCap", 0) / current_price if current_price else 0
        total_debt = bs.get("totalDebt", 0)
        cash = bs.get("cashAndCashEquivalents", 0)
        net_debt = total_debt - cash

        return {
            "ticker": ticker.upper(),
            "company_name": profile.get("companyName", ticker),
            "free_cash_flow": free_cash_flow,
            "current_price": current_price,
            "shares_outstanding": shares_outstanding,
            "net_debt": net_debt,
        }

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None
