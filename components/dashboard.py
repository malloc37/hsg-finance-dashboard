import streamlit as st
import requests
from textblob import TextBlob
from components.options_list import investment_options
from data.finance_api import get_investment_metrics

def spaces(n):
    for i in range(n):
        st.write("")

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
def display_dashboard():
    selected_risk_level = st.session_state.selected_risk_level
    selectionByRisk = []
    with st.form("userSelectedRiskOpion"):
        st.markdown(f"<p class='Assets'>Selection of assets</p>", unsafe_allow_html=True)
        cols = st.columns(len(st.session_state.riskLevelList))
        if selectionByRisk == []:
            for i in range(len(st.session_state.riskLevelList)):
                selectionByRisk.append({"Instrument": "-"})
        for i in range(len(cols)):
            with cols[i]:
                options = [value for value in investment_options[st.session_state.riskLevelList[i]]]
                options.append({"Instrument": "-"})
                selectionByRisk[i] = st.selectbox(
                    st.session_state.riskLevelList[i],
                    options,
                    index=options.index(selectionByRisk[i]),
                    format_func=lambda x: x["Instrument"],
                    key=st.session_state.selected_risk_level[i] + "SelectOption"
                )
        cols2 = st.columns(3)
        with cols2[1]:
            next = st.form_submit_button("Calculate return")
        if {"Instrument": "-"} in selectionByRisk and next:
            st.error("You have to select an option for every risk level.")
        elif next:
            return {
                "next": True,
                "selectionByRisk": selectionByRisk
            }
    spaces(3)
    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown(f"<p class='navigation'>Navigation</p>", unsafe_allow_html=True)
    with col2:
        selected_risk_level = st.selectbox(
            "Risk Level",
            st.session_state.riskLevelList,
            index=st.session_state.riskLevelList.index(selected_risk_level),
            key="risk_level_dropdown"
        )
    selected_option = investment_options[selected_risk_level][0]
    with col3:
        selected_option = st.selectbox(
            "Investment Option",
            investment_options[selected_risk_level],
            index=investment_options[selected_risk_level].index(selected_option),
            format_func=lambda x: x["Instrument"],
            key="investment_option_dropdown"
        )
    st.title("Investment Dashboard")
        
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