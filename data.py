import yfinance as yf
import streamlit as st

def get_company_data(ticker):
    """
    Pulls key financial data for a company from Yahoo Finance.
    Returns a dictionary of the numbers we need for the DCF, or None if
    the ticker is invalid / data is missing.
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        cashflow = stock.cashflow

        if not info or cashflow.empty:
            return None

        # Free cash flow = Operating Cash Flow - Capital Expenditures
        operating_cf = cashflow.loc["Operating Cash Flow"].iloc[0]
        capex = cashflow.loc["Capital Expenditure"].iloc[0]
        free_cash_flow = operating_cf + capex  # capex is usually negative already

        current_price = info.get("currentPrice", 0)
        shares_outstanding = info.get("sharesOutstanding", 0)
        total_debt = info.get("totalDebt", 0)
        cash = info.get("totalCash", 0)
        net_debt = total_debt - cash

        return {
            "ticker": ticker.upper(),
            "company_name": info.get("longName", ticker),
            "free_cash_flow": free_cash_flow,
            "current_price": current_price,
            "shares_outstanding": shares_outstanding,
            "net_debt": net_debt,
        }

    except Exception as e:
        st.error(f"Error fetching data: {e}")
        return None
