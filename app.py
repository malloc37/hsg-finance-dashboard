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
    st.write(f"Initial Investment: €{st.session_state.investment}")
    st.write(f"Monthly Saving Rate: €{st.session_state.monthly}")
    st.write(f"Year Wealth: {st.session_state.yearWealth}")
    st.write(f"riskLevelList: {st.session_state.riskLevelList}")
    st.write(f"SplitRiskLevelList: {st.session_state.SplitRiskLevelList}")
    result = display_input_form()
    if result:
        if result["next"]:
            st.session_state.investment = result["initial_investment"]
            st.session_state.monthly = result["saving_rate"]
            st.session_state.yearWealth = result["time_frame"]
            st.session_state.SplitRiskLevelList = result["risk_split"]
        else:
            st.session_state.action = "previous"

# if user_input:
#     selected_option = display_options_list(user_input)

#     if selected_option:
#         display_dashboard(selected_option)