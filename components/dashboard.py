import streamlit as st
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
def display_dashboard(selected_risk_levels, selected_risk_level=None, selected_option=None):
    st.title("Investment Dashboard")

    if not selected_risk_level:
        selected_risk_level = selected_risk_levels[0]
    if not selected_option:
        selected_option = investment_options[selected_risk_level][0]

    header_col1, header_col2 = st.columns([3, 2])
    with header_col2:
        selected_risk_level = st.selectbox(
            "Risk Level",
            selected_risk_levels,
            index=selected_risk_levels.index(selected_risk_level),
            key="risk_level_dropdown"
        )

        options = investment_options[selected_risk_level]
        selected_option = st.selectbox(
            "Investment Option",
            options,
            format_func=lambda x: x["Instrument"],
            key="investment_option_dropdown"
        )

    with header_col1:
        st.header(f"{selected_option['Instrument']} - {selected_option['Asset Class']}")

    metrics = get_investment_metrics(selected_option["Ticker"], selected_option["Asset Class"])

    st.subheader("Financial Metrics")
    for metric, value in metrics.items():
        if metric == "Price History":
            st.line_chart(value["Close"])
        else:
            st.write(f"**{metric}:** {value}")

    st.subheader("Market Sentiment Analysis")
    headlines = fetch_stock_news(selected_option["Instrument"], "a95a714114e64befabf8b6a87a8a2f8e")
    sentiment_score = analyze_sentiment(headlines)
    sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    st.metric("Sentiment Score", f"{sentiment_score:.2f} ({sentiment_label})")
    st.markdown("### Top News Headlines")
    for headline in headlines:
        st.markdown(f"- {headline}")