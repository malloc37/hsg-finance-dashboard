import streamlit as st
import yfinance as yf
import matplotlib.pyplot as plt
import requests
from textblob import TextBlob

from components.options_list import investment_options
from data.finance_api import get_investment_metrics

def fetch_stock_news(stock_name, api_key):
    params = {
        "q": stock_name,
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
def display_dashboard(selected_risk_levels):
    st.title("Investment Dashboard")

    with st.sidebar:
        st.markdown("### Select Investment Option")
        selected_risk_level = st.selectbox("Risk Level", selected_risk_levels)
        options = investment_options[selected_risk_level]
        selected_option = st.selectbox(
            "Select an Investment Option",
            options,
            format_func=lambda x: x["Instrument"],
        )

    selected_instrument = selected_option.get("Instrument", "Unknown Instrument")
    selected_ticker = selected_option.get("Ticker", "n/a")
    selected_asset_class = selected_option.get("Asset Class", "Unknown Asset Class")

    st.header(f"{selected_instrument} - {selected_asset_class}")

    col1, col2 = st.columns([2, 1])

    with col1:
        if selected_ticker != "n/a":
            data = yf.Ticker(selected_ticker)
            hist = data.history(period="5y")

            st.subheader("Historical Price Trend")
            fig, ax = plt.subplots(figsize=(6, 3))
            ax.plot(hist.index, hist["Close"], label="Close Price", color="skyblue")
            ax.set_title(f"{selected_ticker} Price Trend", fontsize=14)
            st.pyplot(fig)

    with col2:
        st.subheader("Financial Metrics")
        market_cap = data.info.get("marketCap", "N/A")
        dividend_yield = data.info.get("dividendYield", "N/A")
        st.metric("Market Cap", f"${market_cap:,.2f}" if isinstance(market_cap, (int, float)) else "N/A")
        st.metric("Dividend Yield", f"{dividend_yield * 100:.2f}%" if dividend_yield != "N/A" else "N/A")

        st.subheader("Market Sentiment Analysis")
        headlines = fetch_stock_news(selected_instrument, "a95a714114e64befabf8b6a87a8a2f8e")
        sentiment_score = analyze_sentiment(headlines)
        sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
        st.metric("Sentiment Score", f"{sentiment_score:.2f} ({sentiment_label})")

        st.markdown("### Top News Headlines")
        for headline in headlines:
            st.markdown(f"- {headline}")