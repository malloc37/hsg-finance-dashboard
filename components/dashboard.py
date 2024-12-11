import plotly.graph_objects as go
import streamlit as st
import requests
from textblob import TextBlob
from components.options_list import investment_options
from data.finance_api import get_investment_metrics

def spaces(n):
    for _ in range(n):
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

    scaled_sentiment = avg_sentiment * 10
    return scaled_sentiment


def format_metric(label, value):
    """
    Format metrics with appropriate signs and rounding.
    """
    if value == "N/A" or value is None:
        return "Not Available"

    if label in ["Market Cap", "Total Net Assets"]:
        # Convert to billions for readability
        return f"${round(value / 1e9, 2)}B"

    if label in ["Volatility", "Annualized Return", "Dividend Yield", "Expense Ratio", "Yield"]:
        # Percentage values
        return f"{round(value * 100, 2)}%"

    if label == "P/E Ratio" or label == "Duration":
        # Simple rounding
        return f"{round(value, 2)}"

    return value

def display_metrics(metrics, tooltips, asset_class):
    cols = st.columns(3)

    # Define general and specific metrics for the asset class
    general_metrics = [
        ("Market Cap", metrics["Market Cap"]),
        ("Volatility", metrics["Volatility"]),
        ("Annualized Return", metrics["Annualized Return"]),
    ]

    specific_metrics = []
    if asset_class.lower() == "stock":
        specific_metrics = [
            ("P/E Ratio", metrics.get("P/E Ratio", "N/A")),
            ("Dividend Yield", metrics.get("Dividend Yield", "N/A")),
            ("Sector", metrics.get("Sector", "N/A")),
        ]
    elif asset_class.lower() == "etf":
        specific_metrics = [
            ("Expense Ratio", metrics.get("Expense Ratio", "N/A")),
            ("Total Net Assets", metrics.get("Total Net Assets", "N/A")),
            ("Top Holdings", metrics.get("Top Holdings", "N/A")),
        ]
    elif asset_class.lower() == "bonds":
        specific_metrics = [
            ("Yield", metrics.get("Yield", "N/A")),
            ("Duration", metrics.get("Duration", "N/A")),
        ]
    elif asset_class.lower() == "crypto":
        specific_metrics = [
            ("Circulating Supply", metrics.get("Circulating Supply", "N/A")),
            ("24-Hour Volume", metrics.get("24-Hour Volume", "N/A")),
        ]

    all_metrics = general_metrics + specific_metrics

    for i, (label, value) in enumerate(all_metrics):
        tooltip = tooltips.get(label, "No explanation available.")
        formatted_value = format_metric(label, value)
        with cols[i % 3]:
            st.markdown(
                f"""
                <div style='
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    margin-bottom: 10px;
                    padding: 15px;
                    background-color: #DCD7CD;
                    border: 1px solid #110F37;
                    border-radius: 8px;'>
                    <h4 style='text-align: center; color: #110F37; margin: 0;'>
                         &nbsp; {label}
                    </h4>
                    <p style='text-align: center; font-size: 20px; color: #110F37; margin: 0;'>
                        <strong>{formatted_value} &nbsp;&nbsp;&nbsp;</strong>
                    </p>
                </div>
                """,
                unsafe_allow_html=True,
            )
            with st.expander(f"\u2139"):
                st.write(tooltip)

def display_dashboard():
    selectionByRisk = []
    # form to select the final assets, one for each risk level selected.
    with st.form("userSelectedRiskOption"):
        st.markdown("<h2 class = 'assets'>Selection of assets</h2>", unsafe_allow_html=True)
        cols = st.columns(len(st.session_state.riskLevelList))
        if not selectionByRisk:
            for _ in range(len(st.session_state.riskLevelList)):
                selectionByRisk.append({"Instrument": "-"})
        for i, col in enumerate(cols):
            with col:
                options = [value for value in investment_options[st.session_state.riskLevelList[i]]]
                options.append({"Instrument": "-"})
                selectionByRisk[i] = st.selectbox(
                    st.session_state.riskLevelList[i],
                    options,
                    index=options.index(selectionByRisk[i]),
                    format_func=lambda x: x["Instrument"],
                    key=st.session_state.selected_risk_level[i] + "SelectOption",
                )
        submit_col = st.columns(3)[1]
        with submit_col:
            next = st.form_submit_button("Show expected results")
        if {"Instrument": "-"} in selectionByRisk and next:
            st.error("You have to select an option for every risk level.")
        elif next:
            return {
                "next": True,
                "selectionByRisk": selectionByRisk,
                # extract the annualized returns for the selected asset options from Yahoo Finance.
                "irrs": [get_investment_metrics(option["Ticker"], option["Asset Class"])["Annualized Return"] 
                    if option["Instrument"] != "-" 
                    else "" for option in selectionByRisk]
            }
    spaces(4)
    col1, col2, col3 = st.columns(3)
    # creation of the navigation menu to pinpoint the asset option to be displayed with all the correspective metrics.
    selected_risk_level = st.session_state.riskLevelList[0]
    selected_option = investment_options[selected_risk_level][0]
    with col1:
        st.markdown(f"<h2 class='navigation'>Navigation</h2>", unsafe_allow_html=True)
    with col2:
        selected_risk_level = st.selectbox(
            "Risk Level",
            st.session_state.riskLevelList,
            index=st.session_state.riskLevelList.index(selected_risk_level),
            key="risk_level_dropdown",
        )
    with col3:
        selected_option = st.selectbox(
            "Investment Option",
            investment_options[selected_risk_level],
            format_func=lambda x: x["Instrument"],
            key="investment_option_dropdown",
        )
    st.title("Investment Dashboard")
    st.header(f"{selected_option['Instrument']} - {selected_option['Asset Class']}")
    metrics, tooltips = get_investment_metrics(selected_option["Ticker"], selected_option["Asset Class"])

    st.subheader("Short Description")
    st.markdown(
        f"""
        <div style='background-color: #DCD7CD; border: 1px solid #110F37; padding: 15px; border-radius: 8px;'>
            <p style='font-size: 18px; color: #110F37;'>{metrics.get("Short Description", "N/A")}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Financial Metrics")
    display_metrics(metrics, tooltips, selected_option["Asset Class"])
    spaces(2)

    st.subheader("Historical Price Trend")
    if "Price History" in metrics:
        fig = go.Figure()

        fig.add_trace(go.Scatter(
            x=metrics["Price History"].index,
            y=metrics["Price History"]["Close"],
            mode='lines',
            line=dict(color="#375A6A")
        ))

        fig.update_layout(
            plot_bgcolor="#DCD7CD",
            paper_bgcolor="#DCD7CD",
            font=dict(color="#375A6A"),
            xaxis=dict(
                showgrid=True,
                gridcolor="#110F37",
                title="Date",
                titlefont=dict(color="#375A6A"),
                tickfont=dict(color="#375A6A"),
            ),
            yaxis=dict(
                showgrid=True,
                gridcolor="#110F37",
                title="Price",
                titlefont=dict(color="#375A6A"),
                tickfont=dict(color="#375A6A"),
            )
        )

        st.plotly_chart(fig, use_container_width=True)
    spaces(2)

    st.subheader("Market Sentiment Analysis")
    headlines = fetch_stock_news(selected_option["Instrument"], "a95a714114e64befabf8b6a87a8a2f8e")
    sentiment_score = analyze_sentiment(headlines)
    sentiment_label = "Positive" if sentiment_score > 0 else "Negative" if sentiment_score < 0 else "Neutral"
    sentiment_color = (
        "rgba(0, 255, 0, 0.25)" if sentiment_score > 0 else
        "rgba(255, 0, 0, 0.25)" if sentiment_score < 0 else
        "rgba(0, 0, 0, 0.0)"
    )
    st.markdown(
        f"""
        <div style='width: 100%; padding: 15px; background-color: {sentiment_color}; border: 1px solid #375A6A; border-radius: 8px; text-align: left;'>
            <h4 style='color: #110F37;'>Sentiment Score</h4>
            <p style='font-size: 20px; color: #110F37;'><strong>{sentiment_score:.1f} ({sentiment_label})</strong></p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.subheader("Top News Headlines")
    for headline in headlines[:5]:
        st.markdown(
            f"""
            <div style='background-color: #DCD7CD; border: 1px solid #110F37; padding: 10px; margin-bottom: 5px; border-radius: 8px;'>
                <p style='font-size: 16px; color: #110F37;'>{headline}</p>
            </div>
            """,
            unsafe_allow_html=True,
        )