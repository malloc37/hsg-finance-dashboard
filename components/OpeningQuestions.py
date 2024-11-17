import streamlit as st

def displayInvestmentQuestion():
    with st.form("initial_investment_input"):
        col1t, col2t = st.columns([5, 0.1])
        with col1t:
            st.title("How much are you looking to invest?")
        with col2t:
            st.write("🛈")
        investment = st.number_input("(CHF)", min_value=0.0, step=10.0)
        next = st.form_submit_button("Next")
        with st.expander("🛈"):
            st.write("Banks suggest investing 1/3 in the market and keeping 2/3 in other assets or liquid reserves for stability.")
        if next:
            return {
                "next": True,
                "initial_investment": investment
            }
    return None

def displayMonthlySavingQuestion():
    with st.form("saving_rate_input"):
        col1t, col2t = st.columns([5, 0.1])
        with col1t:
            st.title("What portion of your monthly savings are you considering allocating to market investments?")
        with col2t:
            st.write("🛈")
        monthly = st.number_input("(CHF)", min_value=0.0, step=10.0)
        col1, col2 = st.columns([1, 5])
        with col1:
            previous = st.form_submit_button("Previous")
        with col2:
            next = st.form_submit_button("Next")
        with st.expander("🛈"):
            st.write("Allocate 5-10% of your monthly income to market investments, as it aligns to the 50/30/20 rule, dividing your income into 50% for essentials, 30% for discretionary spending, and 20% for savings and investments.")
        if next:
            return {
                "next": True,
                "saving_rate": monthly
            }
        if previous:
            return {
                "next": False,
                "saving_rate": -10
            }
    return None

def displayYearWealthQuestion():
    with st.form("yearWealth_input"):
        col1t, col2t = st.columns([5, 0.1])
        with col1t:
            st.title("When do you plan to cash out and enjoy your wealth?")
        with col2t:
            st.write("🛈")
        col11, col22 = st.columns(2)
        with col11:
            year = st.number_input("Years", min_value=1, step=1, value=1)
        with col22:
            month = st.number_input("Months", min_value=1, step=1, max_value=11, value=1)
        col1, col2 = st.columns([1, 5])
        with col1:
            previous = st.form_submit_button("Previous")
        with col2:
            next = st.form_submit_button("Next")
        with st.expander("🛈"):
            st.write("Most financial strategies align exit timing with investment maturity cycles, typically between 5-10 years for market assets.")
        if next:
            return {
                "next": True,
                "yearWealth": month + year*12
            }
        if previous:
            return {
                "next": False,
                "yearWealth": -1
            }
    return None

def displayRiskLevelQuestion():
    with st.form("riskLevel_input"):
        col1t, col2t = st.columns([5, 0.1])
        with col1t:
            st.title("At which risk levels would you like to invest?")
        with col2t:
            st.write("🛈")
        options = ["Very-low risk", "Low risk", "Moderate risk", "High risk", "Very-high risk"]
        
        selected_options = st.multiselect(
            "Please select up to three options.",
            options
        )
        col1, col2 = st.columns([1, 5])
        with col1:
            previous = st.form_submit_button("Previous")
        with col2:
            next = st.form_submit_button("Next")
        with st.expander("🛈"):
            st.write("Spreading your investments across different industries, geographies, asset types, and risk levels is recommended by the Diversification principle, mitigating the impact of specific crises on your portfolio.")
        if len(selected_options) > 3:
            st.error("You can select a maximum of 3 options. Please deselect some options.")
        elif next and len(selected_options) < 1:
            st.error("You have to select a minimum of 1 option. Please select at least one options.")
        elif next:
            return {
                "next": True,
                "riskLevelList": [option for option in options if option in selected_options]
            }
        elif previous:
            return {
                "next": False,
                "riskLevelList": []
            }
    return None

def displaySplitRiskLevelQuestion(riskLevelList):
    with st.form("splitRiskLevel_input"):
        col1t, col2t = st.columns([5, 0.1])
        with col1t:
            st.title("Please allocate the investment amount in percentages across the selected risk levels")
        with col2t:
            st.write("🛈")
        split_1 = 0
        split_2 = 0 
        split_3 = 0
        if len(riskLevelList) > 0:
            split_1 = st.slider(riskLevelList[0] + " allocation (%)", 0, 100, 0, step=1, key=riskLevelList[0])
        if len(riskLevelList) > 1:
            split_2 = st.slider(riskLevelList[1] + " allocation (%)", 0, 100, 0, step=1, key=riskLevelList[1])
        if len(riskLevelList) > 2:
            split_3 = st.slider(riskLevelList[2] + " allocation (%)", 0, 100, 0, step=1, key=riskLevelList[2])
        col1, col2 = st.columns([1, 5])
        with col1:
            previous = st.form_submit_button("Previous")
        with col2:
            next = st.form_submit_button("Next")
        with st.expander("🛈"):
            st.write("The 100 investing rule suggests allocating 100 minus your age to medium to high-risk investments (risk levels 3 to 5), with the remainder in low-risk options (risk levels 1 & 2).")
        if split_1 + split_2 + split_3 != 100 and next:
            st.error("The total allocation across all risk levels must sum up to 100%. Please adjust the sliders.")
        elif next:
            return {
                "next": True,
                "SplitRiskLevelList": [split_1, split_2, split_3][:len(riskLevelList)]
            }
        elif previous:
            return {
                "next": False,
                "SplitRiskLevelList": []
            }
    return None