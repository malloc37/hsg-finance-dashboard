import streamlit as st
from components.input_form import display_input_form
from components.dashboard import display_dashboard
from components.openingQuestions import *
from utils.styling import *
from components.returns import displayReturns

# Set the Streamlit app configuration: page title and layout
st.set_page_config(page_title="Investment Advisor Dashboard", layout="wide")

# Initialize session state variables for persisting data across pages
def initialize_state():
    if "counter" not in st.session_state:  # Tracks the current page
        st.session_state.counter = 0
    if "investment" not in st.session_state:  # Initial investment value
        st.session_state.investment = 0
    if "monthly" not in st.session_state:  # Monthly savings input
        st.session_state.monthly = 0
    if "yearWealth" not in st.session_state:  # Investment duration (months)
        st.session_state.yearWealth = 0
    if "riskLevelList" not in st.session_state:  # List of selected risk levels
        st.session_state.riskLevelList = []
    if "SplitRiskLevelList" not in st.session_state:  # Split percentages per risk level
        st.session_state.SplitRiskLevelList = []
    if "action" not in st.session_state:  # Tracks navigation actions (e.g., next/previous)
        st.session_state.action = None
    if "selected_risk_level" not in st.session_state:  # Selected risk level
        st.session_state.selected_risk_level = None
    if "selected_option" not in st.session_state:  # Selected investment option
        st.session_state.selected_option = None
    if "selectionByRisk" not in st.session_state:  # User-selected assets per risk level
        st.session_state.selectionByRisk = []
    if "irrs" not in st.session_state:  # Annualized return rates of selected investments
        st.session_state.irrs = []

def spaces(n):
    for i in range(n):
        st.write("")

initialize_state()

# Update the current page based on the navigation action (next/previous)
if st.session_state.action == "next":
    st.session_state.counter += 1
    st.session_state.action = None
elif st.session_state.action == "previous":
    st.session_state.counter -= 1
    st.session_state.action = None

# Display pages dynamically based on the counter value
if st.session_state.counter == 0:
    apply_custom_styling()
    spaces(4)
    result = displayInvestmentQuestion()  # Page to input initial investment
    if result and result["next"]:
        st.session_state.investment = result["initial_investment"]
        st.session_state.action = "next"

if st.session_state.counter == 1:
    apply_custom_styling()
    spaces(4)
    result = displayMonthlySavingQuestion()  # Page to input monthly savings
    if result:
        if result["next"]:
            st.session_state.monthly = result["saving_rate"]
            st.session_state.action = "next"
        else:
            st.session_state.action = "previous"

if st.session_state.counter == 2:
    apply_custom_styling()
    spaces(4)
    result = displayYearWealthQuestion()  # Page to input investment term
    if result:
        if result["next"]:
            st.session_state.yearWealth = result["yearWealth"]
            st.session_state.action = "next"
        else:
            st.session_state.action = "previous"

if st.session_state.counter == 3:
    apply_custom_styling()
    spaces(4)
    result = displayRiskLevelQuestion()  # Page to choose risk levels
    if result:
        if result["next"]:
            st.session_state.riskLevelList = result["riskLevelList"]
            st.session_state.action = "next"
        else:
            st.session_state.action = "previous"

if st.session_state.counter == 4:
    apply_custom_styling()
    spaces(4)
    result = displaySplitRiskLevelQuestion(st.session_state.riskLevelList)  # Page to split risk levels
    if result:
        if result["next"]:
            st.session_state.SplitRiskLevelList = result["SplitRiskLevelList"]
            st.session_state.action = "next"
            st.session_state.selected_risk_level = st.session_state.riskLevelList[0]
        else:
            st.session_state.action = "previous"

if st.session_state.counter == 5:
    result = display_input_form()  # Page to input investment details
    if result:
        if result["next"]:
            # Save user inputs into session state
            st.session_state.investment = result["initial_investment"]
            st.session_state.monthly = result["saving_rate"]
            st.session_state.yearWealth = result["time_frame"]
            st.session_state.SplitRiskLevelList = result["risk_split"]
        else:
            st.session_state.action = "previous"
    if st.session_state.riskLevelList and st.session_state.SplitRiskLevelList:
        custom_stylingDashboard()
        resultDash = display_dashboard()  # Display the main investment dashboard
        if resultDash:
            if resultDash["next"]:
                st.session_state.selectionByRisk = resultDash["selectionByRisk"]
                st.session_state.action = "next"
                st.session_state.irrs = resultDash["irrs"]
    else:
        # Display an error if risk levels or allocations are incomplete
        st.error("No risk levels or allocations selected. Please go back and complete the steps.")

if st.session_state.counter == 6:
    custom_stylingReturn()
    result = displayReturns()  # Display expected returns summary
    if result:
        if not result["next"]:
            st.session_state.action = "previous"