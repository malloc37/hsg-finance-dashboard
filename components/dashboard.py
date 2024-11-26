import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import requests
from textblob import TextBlob

def fetch_stock_news(stock_ticker, api_key):
    params = {
        "q": stock_ticker,
        "language": "en",
        "sortBy": "relevancy",
        "pageSize": 5,
        "apiKey": api_key
    }

    url = "https://newsapi.org/v2/everything"
    response = requests.get(url, params=params)

    if response.status_code == 200:
        articles = response.json().get("articles", [])
        return [article["title"] for article in articles]
    else:
        st.error("Error fetching news articles. Please check the API key or request.")
        return []

def analyze_sentiment(headlines):
    sentiment_scores = [TextBlob(headline).sentiment.polarity for headline in headlines]
    avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
    return avg_sentiment


def display_dashboard(selected_option, initial_investment, monthly_contribution, investment_period, allocation):
    with st.sidebar:
        st.title("Investment Dashboard Menu")
        st.markdown("### Summary")
        initial_investment = st.number_input(
            "Initial Investment (€)",
            value=initial_investment,
            min_value=0.0,
            step=10.0
        )
        monthly_contribution = st.number_input(
            "Monthly Contribution (€)",
            value=monthly_contribution,
            min_value=0.0,
            step=10.0
        )
        investment_period = st.number_input(
            "Investment Period (months)",
            value=investment_period,
            min_value=1,
            step=1
        )
        st.markdown("---")
        st.markdown("### Actions")
        if st.button("Back to Input"):
            st.session_state.counter -= 1

    st.title("Investment Dashboard")

    selected_instrument = selected_option.get("Instrument", "Unknown Instrument")
    selected_ticker = selected_option.get("Ticker", "n/a")
    selected_risk_level = selected_option.get("Risk Level", "Unknown Risk Level")

    st.header(f"{selected_instrument} - {selected_risk_level}")

    col1, col2 = st.columns([2, 1])

    with col1:
        if selected_ticker != "n/a":
            data = yf.Ticker(selected_ticker)
            hist = data.history(period="5y")

            st.subheader("Historical Price Trend")
            fig, ax = plt.subplots(figsize=(6, 3))
            fig.patch.set_facecolor('#f0f0f0')
            ax.set_facecolor('#e0e0e0')
            ax.plot(hist.index, hist["Close"], label="Close Price", color="skyblue")
            ax.set_title(f"{selected_ticker} Price Trend", fontsize=14, color="#1f3b4d")
            ax.set_xlabel("Year", fontsize=12, color="#1f3b4d")
            ax.set_ylabel("Price ($)", fontsize=12, color="#1f3b4d")
            ax.grid(True, color='#1f3b4d', linestyle='--', linewidth=0.5)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)
            ax.spines['left'].set_color('#1f3b4d')
            ax.spines['bottom'].set_color('#1f3b4d')
            ax.tick_params(axis='x', colors='#1f3b4d')
            ax.tick_params(axis='y', colors='#1f3b4d')
            st.pyplot(fig)

    with col2:
        st.subheader("Financial Metrics")
        market_cap = data.info.get("marketCap", "N/A")
        dividend_yield = data.info.get("dividendYield", "N/A")
        beta = data.info.get("beta", "N/A")

        st.metric("Market Cap", f"${market_cap:,.2f}" if isinstance(market_cap, (int, float)) else "N/A")
        st.metric("Dividend Yield", f"{dividend_yield * 100:.2f}%" if dividend_yield != "N/A" else "N/A")
        st.metric("Beta", beta)


        st.subheader("Market Sentiment Analysis")
        headlines = fetch_stock_news(selected_ticker, "a95a714114e64befabf8b6a87a8a2f8e")
        sentiment_score = analyze_sentiment(headlines)
        sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
        st.metric("Sentiment Score", f"{sentiment_score:.2f} ({sentiment_label})")

        st.markdown("### Top News Headlines")
        for headline in headlines:
            st.markdown(f"- {headline}")


    st.markdown("---")
    st.subheader("Investment Summary")
    col1, col2, col3 = st.columns(3)
    col1.metric("Initial Investment", f"€{initial_investment:,.2f}")
    col2.metric("Monthly Contribution", f"€{monthly_contribution:,.2f}")
    col3.metric("Investment Period", f"{investment_period} months")

    st.markdown("### Portfolio Allocation")
    allocation_summary = "\n".join([f"- {risk}: {percentage}%" for risk, percentage in allocation.items()])
    st.markdown(f"**Allocation Summary:**\n{allocation_summary}")