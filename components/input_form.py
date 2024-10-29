import streamlit as st

def display_input_form():
    with st.sidebar.form("user_input"):
        risk_level = st.selectbox("Select Risk Level", ["1 - Very Low", "2 - Low", "3 - Moderate", "4 - High", "5 - Very High"])
        saving_rate = st.number_input("Enter Your Monthly Saving Rate (€)", min_value=0.0, step=10.0)
        initial_investment = st.number_input("Initial Investment Amount (€)", min_value=0.0, step=100.0)
        time_frame = st.number_input("Investment Time Frame (years)", min_value=1, step=1)

        # individual risk level sliders
        split_very_low = st.slider("Risk Level 1 Split (%)", 0, 100, 0, step=1, key="split_very_low")
        split_low = st.slider("Risk Level 2 Split (%)", 0, 100, 0, step=1, key="split_low")
        split_moderate = st.slider("Risk Level 3 Split (%)", 0, 100, 0, step=1, key="split_moderate")
        split_high = st.slider("Risk Level 4 Split (%)", 0, 100, 0, step=1, key="split_high")
        split_very_high = st.slider("Risk Level 5 Split (%)", 0, 100, 0, step=1, key="split_very_high")

        # check if total allocation exceeds 100%
        total_allocation = split_very_low + split_low + split_moderate + split_high + split_very_high
        if total_allocation > 100:
            st.error("The total allocation across all risk levels cannot exceed 100%. Please adjust the sliders.")

        submitted = st.form_submit_button("Get Investment Options")

        if submitted and total_allocation <= 100:
            return {
                "risk_level": risk_level,
                "saving_rate": saving_rate,
                "initial_investment": initial_investment,
                "time_frame": time_frame,
                "risk_split": {
                    "very_low": split_very_low,
                    "low": split_low,
                    "moderate": split_moderate,
                    "high": split_high,
                    "very_high": split_very_high
                }
            }
    return None