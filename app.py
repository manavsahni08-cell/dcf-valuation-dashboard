import streamlit as st
import pandas as pd
from data import get_company_data
from dcf_model import run_dcf, sensitivity_table

st.set_page_config(page_title="DCF Valuation Dashboard", layout="wide")
st.title("📊 Interactive DCF Valuation Dashboard")
st.caption("Enter a stock ticker and adjust assumptions to see an implied fair value.")

ticker = st.text_input("Enter a stock ticker (e.g. AAPL, MSFT, TSCO.L)", "AAPL")

col1, col2, col3 = st.columns(3)
wacc = col1.slider("WACC (discount rate)", 0.04, 0.15, 0.09, 0.005)
growth_rate = col2.slider("FCF growth rate (years 1-5)", 0.00, 0.20, 0.06, 0.005)
terminal_growth = col3.slider("Terminal growth rate", 0.00, 0.05, 0.025, 0.0025)

if st.button("Run Valuation"):
    data = get_company_data(ticker)

    if data is None:
        st.error("Couldn't find data for that ticker. Try another one.")
    else:
        result = run_dcf(
            data["free_cash_flow"], wacc, growth_rate, terminal_growth,
            data["net_debt"], data["shares_outstanding"]
        )

        st.subheader(f"{data['company_name']} ({data['ticker']})")

        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"${data['current_price']:.2f}")
        col2.metric("Implied Fair Value", f"${result['implied_share_price']:.2f}")
        upside = (result['implied_share_price'] / data['current_price'] - 1) * 100
        col3.metric("Upside/Downside", f"{upside:.1f}%")

        st.subheader("Projected Free Cash Flow")
        fcf_df = pd.DataFrame({
            "Year": [f"Year {i}" for i in range(1, 6)],
            "Projected FCF ($)": result["projected_fcf"],
        })
        st.line_chart(fcf_df.set_index("Year"))

        st.subheader("Sensitivity: Implied Share Price")
        wacc_range = [wacc - 0.02, wacc - 0.01, wacc, wacc + 0.01, wacc + 0.02]
        growth_range = [terminal_growth - 0.01, terminal_growth - 0.005, terminal_growth, terminal_growth + 0.005, terminal_growth + 0.01]
        table = sensitivity_table(data["free_cash_flow"], data["net_debt"], data["shares_outstanding"], wacc_range, growth_range)

        sens_df = pd.DataFrame(
            table,
            index=[f"WACC {w*100:.1f}%" for w in wacc_range],
            columns=[f"TGR {g*100:.2f}%" for g in growth_range],
        )
        st.dataframe(sens_df.style.format("${:.2f}"))
