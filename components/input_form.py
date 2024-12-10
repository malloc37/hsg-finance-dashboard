import streamlit as st
from components.options_list import investment_options

# lateral menu as a summarise of the initial five inputs, with the possibility to edit all of them excluding the risk levels selected.
def display_input_form():
    with st.sidebar.form("user_input"):
        initial_investment = st.number_input("Starting capital (CHF)", min_value=0.0, step=10.0, value=st.session_state.investment)
        saving_rate = st.number_input("Monthly contribution (CHF)", min_value=0.0, step=10.0, value=st.session_state.monthly)
        time_frame = st.number_input("Investment time frame (months)", min_value=1, step=1, value=st.session_state.yearWealth)
        split_1 = 0
        split_2 = 0
        split_3 = 0
        if len(st.session_state.riskLevelList) > 0:
            split_1 = st.slider(st.session_state.riskLevelList[0] + " allocation (%)", 0, 100, step=1, 
                                key=st.session_state.riskLevelList[0], value=st.session_state.SplitRiskLevelList[0])
        if len(st.session_state.riskLevelList) > 1:
            split_2 = st.slider(st.session_state.riskLevelList[1] + " allocation (%)", 0, 100, step=1, 
                                key=st.session_state.riskLevelList[1], value=st.session_state.SplitRiskLevelList[1])
        if len(st.session_state.riskLevelList) > 2:
            split_3 = st.slider(st.session_state.riskLevelList[2] + " allocation (%)", 0, 100, step=1, 
                                key=st.session_state.riskLevelList[2], value=st.session_state.SplitRiskLevelList[2])
        next = st.form_submit_button("Change")
        previous = st.form_submit_button("Back to questions")
        if split_1 + split_2 + split_3 != 100 and next:
            st.error("The total allocation across all risk levels must sum up to 100%. Please adjust the sliders.")
        elif next and ((split_1 == 0)  or (split_2 == 0 and len(st.session_state.riskLevelList) > 1) or (split_3 == 0 and len(st.session_state.riskLevelList) > 2)):
            st.error("Every risk level must have at least 1% allocated. Please adjust the sliders.")
        elif next and initial_investment <= 0:
            st.error("The initial investment must be greater than zero.")
        elif next and saving_rate <= 0:
            st.error("The monthly contribution must be greater than zero.")
        elif next and time_frame <= 0:
            st.error("The investment period must be greater than zero.")
        elif next:
            return {
                "next": True,
                "initial_investment": initial_investment,
                "saving_rate": saving_rate,
                "time_frame": time_frame,
                "risk_split": [split_1, split_2, split_3][:len(st.session_state.riskLevelList)]
            }
        elif previous:
            return {
                "next": False
            }
    return None