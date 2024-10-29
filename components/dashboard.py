import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt

def display_dashboard(option):
    ticker = option["Ticker"]
    st.title(f"Dashboard for {option['Instrument']}")

    if ticker != "n/a":
        data = yf.Ticker(ticker)
        hist = data.history(period="5y")

        st.subheader("Historical Price Trend")
        fig, ax = plt.subplots(figsize=(10, 5))
        fig.patch.set_facecolor('#f0f0f0')
        ax.set_facecolor('#e0e0e0')

        # plotting data with customized styles
        ax.plot(hist.index, hist["Close"], label="Close Price", color="skyblue")
        ax.set_title(f"{ticker} Price Trend", fontsize=16, color="#1f3b4d")
        ax.set_xlabel("Year", fontsize=12, color="#1f3b4d")
        ax.set_ylabel("Price ($)", fontsize=12, color="#1f3b4d")

        # customize grid and spines with dark blue color
        ax.grid(True, color='#1f3b4d', linestyle='--', linewidth=0.5)
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color('#1f3b4d')
        ax.spines['bottom'].set_color('#1f3b4d')
        ax.tick_params(axis='x', colors='#1f3b4d')
        ax.tick_params(axis='y', colors='#1f3b4d')

        st.pyplot(fig)

        st.subheader("Financials")

        # fetching the financial metrics
        market_cap = data.info.get("marketCap", "N/A")
        dividend_yield = data.info.get("dividendYield", "N/A")
        beta = data.info.get("beta", "N/A")

        # display financial metrics in columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Market Cap", f"{market_cap:,}")
        col2.metric("Dividend Yield", f"{dividend_yield * 100:.2f}%" if dividend_yield != "N/A" else "N/A")
        col3.metric("Beta", beta)