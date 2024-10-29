import streamlit as st

investment_options = {
    "1 - Very Low": [
        {"Instrument": "Savings Account", "Ticker": "n/a", "Details": "High liquidity, virtually risk-free"}
    ],
    "2 - Low": [
        {"Instrument": "iShares 7-10 Year Treasury Bond ETF", "Ticker": "IEF", "Details": "U.S. Treasury Bond ETF"}
    ],
    "3 - Moderate": [
        {"Instrument": "Vanguard S&P 500 ETF", "Ticker": "VOO", "Details": "S&P 500 Index Fund"}
    ],
    "4 - High": [
        {"Instrument": "Tesla Stock", "Ticker": "TSLA", "Details": "High growth EV company"}
    ],
    "5 - Very High": [
        {"Instrument": "Bitcoin", "Ticker": "BTC-USD", "Details": "Highly volatile cryptocurrency"}
    ]
}

def display_options_list(user_input):
    st.subheader(f"Investment Options for Risk Level {user_input['risk_level']}")
    options = investment_options[user_input["risk_level"]]
    selected_option = st.selectbox("Select an Investment Option", options, format_func=lambda x: x["Instrument"])
    return selected_option