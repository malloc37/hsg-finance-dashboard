import streamlit as st
from components.dashboard import spaces
import datetime
from dateutil.relativedelta import relativedelta
import numpy_financial as npf

# Finincial Formula to calculate the expected total future value (principal + interest) of only the monthly recurring contributions.
def futureValueFun():
    futureValue = 0
    for i in range(len(st.session_state.SplitRiskLevelList)):
        futureValue += ((st.session_state.monthly * st.session_state.SplitRiskLevelList[i] / 100) 
                    * ((1 + (st.session_state.irrs[i] / 12)) ** (st.session_state.yearWealth) - 1) / (st.session_state.irrs[i] / 12))
    return futureValue

# Finincial Formula to calculate the expected total future value (principal + interest) of only the initial investment (I_0).
def initialInvInterestPartialFun():
    initialInvInterest = 0
    for i in range(len(st.session_state.SplitRiskLevelList)):
        initialInvInterest += (st.session_state.investment * st.session_state.SplitRiskLevelList[i] / 100) * (1 + st.session_state.irrs[i] / 12)**(st.session_state.yearWealth)
    return initialInvInterest

def displayReturns():
    with st.form("returnsForm"):
        st.title("Expected return")
        spaces(2)
        col1, col2, col3, col4, col5 = st.columns([3,0.2,3,0.2,3])
        now = datetime.datetime.now()
        
        # Summary of the inputted value, specifically. Initial investment, Monthly saving, Investment term, Invested savings, Total invested 
        with col1:
            st.markdown(f"<p class='subTitle'>Summary - {now.strftime('%b %Y')}</p>", unsafe_allow_html=True)
            col11, col22, col33 = st.columns([3.4, 0.2, 4])
            with col11:
                st.markdown(f"<p class='name'>Initial investment</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Monthly saving</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Investment term</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Invested savings</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameRe'>Total invested</p>", unsafe_allow_html=True)
            with col22:
                for _ in range(4):
                    st.markdown(f"<p class='twoPoints'>:</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='twoPointsRe'>:</p>", unsafe_allow_html=True)
            with col33:
                initialInvestment = st.session_state.investment
                st.markdown(f"<p class='value'>CHF {"{:,.0f}".format(initialInvestment)}</p>", unsafe_allow_html=True)
                monthlySaving = st.session_state.monthly
                st.markdown(f"<p class='value'>CHF {"{:,.0f}".format(monthlySaving)}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='value'>{st.session_state.yearWealth} months</p>", unsafe_allow_html=True)
                # formula to calculate 'Invested savings'
                totInvestedSaving = st.session_state.monthly * st.session_state.yearWealth
                st.markdown(f"<p class='value'>CHF {"{:,.0f}".format(totInvestedSaving)}</p>", unsafe_allow_html=True)
                # formula to calculate 'Total invested'
                totalInvested = st.session_state.monthly * st.session_state.yearWealth + st.session_state.investment
                st.markdown(f"<p class='valueRe'>CHF {"{:,.0f}".format(totalInvested)}</p>", unsafe_allow_html=True)
        
        # arrows' columns
        with col2:
            spaces(1)
            st.write("\u2192")
            spaces(3)
            st.write("\u2192")
        with col4:
            spaces(1)
            st.write("\u2192")
            spaces(3)
            st.write("\u2192")
        
        # column with Initial inv. gains, Savings' gains, Avg. risk of inv, Total gains, Total value
        with col5:
            st.markdown(f"<p class='subTitle'>Expected value - {(now + relativedelta(months=st.session_state.yearWealth)).strftime('%b %Y')}</p>", unsafe_allow_html=True)
            col111, col222, col333 = st.columns([3.4, 0.2, 4])
            with col111:
                st.markdown(f"<p class='name'>Initial inv. gains</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Savings' gains</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Avg. risk of inv.</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameGr'>Total gains</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameGr'>Total value</p>", unsafe_allow_html=True)
            with col222:
                for i in range(3):
                    st.markdown(f"<p class='twoPoints'>:</p>", unsafe_allow_html=True)
                for i in range(2):
                    st.markdown(f"<p class='twoPointsGr'>:</p>", unsafe_allow_html=True)
            with col333:
                # formula to calculate 'Initial inv. gains'
                initialInvInterest = initialInvInterestPartialFun() - initialInvestment
                st.markdown(f"<p class='value'>CHF {'{:,.2f}'.format(initialInvInterest)}</p>", unsafe_allow_html=True)
                # formula to calculate 'Savings' gains'
                savingInterest = futureValueFun() - totInvestedSaving
                st.markdown(f"<p class='value'>CHF {'{:,.2f}'.format(savingInterest)}</p>", unsafe_allow_html=True)
                # formula to calculate 'Avg. risk of inv.', considering both the risk level selections and the duration of the investment
                avgRiskOfInv = 0
                for i in range(len(st.session_state.riskLevelList)):
                    if st.session_state.riskLevelList[i] == "Very-low risk":
                        avgRiskOfInv += 1 * st.session_state.SplitRiskLevelList[i]
                    elif st.session_state.riskLevelList[i] == "Low risk":
                        avgRiskOfInv += 2 * st.session_state.SplitRiskLevelList[i]
                    elif st.session_state.riskLevelList[i] == "Moderate risk":
                        avgRiskOfInv += 3 * st.session_state.SplitRiskLevelList[i]
                    elif st.session_state.riskLevelList[i] == "High risk":
                        avgRiskOfInv += 4 * st.session_state.SplitRiskLevelList[i]
                    elif st.session_state.riskLevelList[i] == "Very-high risk":
                        avgRiskOfInv += 5 * st.session_state.SplitRiskLevelList[i]    
                avgRiskOfInv = avgRiskOfInv / 100
                timeFactorOfRisk = avgRiskOfInv + (1 - (st.session_state.yearWealth / 120))
                avgRiskOfInv = avgRiskOfInv if st.session_state.yearWealth > 120 else timeFactorOfRisk if timeFactorOfRisk < 5 else 5
                st.markdown(f"<p class='value'>{'{:,.2f}'.format(avgRiskOfInv)}</p>", unsafe_allow_html=True)
                # formula to calculate 'Total gains'
                totalInterest = savingInterest + initialInvInterest
                st.markdown(f"<p class='valueGr'>CHF {'{:,.2f}'.format(totalInterest)}</p>", unsafe_allow_html=True)
                # formula to calculate 'Total value'
                totalValue = totalInterest + totalInvested
                st.markdown(f"<p class='valueGr'>CHF {'{:,.2f}'.format(totalInterest + totalInvested)}</p>", unsafe_allow_html=True)
        
        # column with CAGR and ROR.
        with col3:
            col3_1, col3_2 = st.columns([2.2,1])
            with col3_1:
                st.markdown(f"<p class='subTitleM'>Return rates</p>", unsafe_allow_html=True)
            with col3_2:
                st.write('\u2139')
            col1111, col2222, col3333 = st.columns([3.4, 0.2, 4])
            with col1111:
                st.markdown(f"<p class='name'></p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameG'>CAGR</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'></p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameG'>ROR</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'></p>", unsafe_allow_html=True)
            with col2222:
                st.markdown(f"<p class='twoPoints'></p>", unsafe_allow_html=True)
                st.markdown(f"<p class='twoPointsG'>:</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='twoPoints'></p>", unsafe_allow_html=True)
                st.markdown(f"<p class='twoPointsG'>:</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='twoPoints'></p>", unsafe_allow_html=True)
            with col3333:
                st.markdown(f"<p class='value'></p>", unsafe_allow_html=True)
                # formula to calculate 'CAGR'
                cagr = (totalValue / totalInvested) ** (1 / (st.session_state.yearWealth / 12)) - 1
                st.markdown(f"<p class='valueG'>{'{:,.2f}'.format((cagr * 100))}%</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='value'></p>", unsafe_allow_html=True)
                # formula to calculate 'ROR'
                ror = (totalValue - totalInvested) / (totalInvested)
                st.markdown(f"<p class='valueG'>{'{:,.2f}'.format((ror * 100))}%</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='value'></p>", unsafe_allow_html=True)
        spaces(2)
        previous = st.form_submit_button("Previous")
        if previous:
            return {
                "next": False
            }
    with st.expander('\u2139'):
        st.write("CAGR is the annualized growth rate showing how much your investment would have grown each year if it had grown at a steady pace and is used to compare investments on ayearly growth.")
        st.write("ROR is the total return on your investment over a period, considering both the initial capital and contributions, and is used to measure your earnings relative to your total contribution.")
        