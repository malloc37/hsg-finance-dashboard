import streamlit as st
from components.input_form import display_input_form
from components.options_list import display_options_list
from components.dashboard import display_dashboard
from components.OpeningQuestions import *
from utils.styling import apply_custom_styling

# toDO: double click problem

st.set_page_config(page_title="Investment Advisor Dashboard", layout="wide")

def initialize_state():
    if "counter" not in st.session_state:
        st.session_state.counter = 0
    if "investment" not in st.session_state:
        st.session_state.investment = 0
    if "monthly" not in st.session_state:
        st.session_state.monthly = 0
    if "yearWealth" not in st.session_state:
        st.session_state.yearWealth = 0
    if "riskLevelList" not in st.session_state:
        st.session_state.riskLevelList = []
    if "SplitRiskLevelList" not in st.session_state:
        st.session_state.SplitRiskLevelList = []
    if "action" not in st.session_state:
        st.session_state.action = None

initialize_state()
apply_custom_styling()

if st.session_state.action == "next":
    st.session_state.counter += 1
    st.session_state.action = None
elif st.session_state.action == "previous":
    st.session_state.counter -= 1
    st.session_state.action = None

for i in range(4):
    st.write("")

if st.session_state.counter == 0:
    result = displayInvestmentQuestion()
    if result and result["next"]:
        st.session_state.investment = result["initial_investment"]
        st.session_state.action = "next"
if st.session_state.counter == 1:
    result = displayMonthlySavingQuestion()
    if result:
        if result["next"]:
            st.session_state.monthly = result["saving_rate"]
            st.session_state.action = "next"
        else:
            st.session_state.action = "previous"
if st.session_state.counter == 2:
    result = displayYearWealthQuestion()
    if result:
        if result["next"]:
            st.session_state.yearWealth = result["yearWealth"]
            st.session_state.action = "next"
        else:
            st.session_state.action = "previous"
if st.session_state.counter == 3:
    result = displayRiskLevelQuestion()
    if result:
        if result["next"]:
            st.session_state.riskLevelList = result["riskLevelList"]
            st.session_state.action = "next"
        else:
            st.session_state.action = "previous"
if st.session_state.counter == 4:
    result = displaySplitRiskLevelQuestion(st.session_state.riskLevelList)
    if result:
        if result["next"]:
            st.session_state.SplitRiskLevelList = result["SplitRiskLevelList"]
            st.session_state.action = "next"
        else:
            st.session_state.action = "previous"
if st.session_state.counter == 5:
    if st.session_state.riskLevelList and st.session_state.SplitRiskLevelList:
        selected_risk_level = st.session_state.riskLevelList[0]
        investment_options = {
            "Very-low risk": {"Instrument": "Savings Account", "Ticker": "n/a", "Risk Level": "Very Low"},
            "Low risk": {"Instrument": "iShares 7-10 Year Treasury Bond ETF", "Ticker": "IEF",
                         "Risk Level": "Low Risk"},
            "Moderate risk": {"Instrument": "Tesla Stock", "Ticker": "TSLA", "Risk Level": "Moderate Risk"},
            "High risk": {"Instrument": "Vanguard S&P 500 ETF", "Ticker": "VOO", "Risk Level": "High Risk"},
            "Very-high risk": {"Instrument": "Bitcoin", "Ticker": "BTC-USD", "Risk Level": "Very High Risk"}
        }

        selected_option = investment_options.get(selected_risk_level, {"Instrument": "N/A", "Ticker": "n/a"})

        allocation = {
            risk: st.session_state.SplitRiskLevelList[i]
            for i, risk in enumerate(st.session_state.riskLevelList)
        }

        display_dashboard(
            selected_option=selected_option,
            initial_investment=st.session_state.investment,
            monthly_contribution=st.session_state.monthly,
            investment_period=st.session_state.yearWealth,
            allocation=allocation
        )
    else:
        st.error("No risk levels or allocations selected. Please go back and complete the steps.")
