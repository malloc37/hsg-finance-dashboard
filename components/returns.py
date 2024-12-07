import streamlit as st
from components.dashboard import spaces
import datetime
from dateutil.relativedelta import relativedelta
import numpy_financial as npf

def futureValueFun(irrs):
    savingInterest = 0
    for i in range(len(st.session_state.SplitRiskLevelList)):
        savingInterest += ((st.session_state.monthly * st.session_state.SplitRiskLevelList[i] / 100) 
                    * ((1 + (irrs[i] / 12)) ** (st.session_state.yearWealth) - 1) / (irrs[i] / 12))
    return savingInterest

def initialInvInterestPartialFun(irrs):
    initialInvInterest = 0
    for i in range(len(st.session_state.SplitRiskLevelList)):
        initialInvInterest += (st.session_state.investment * st.session_state.SplitRiskLevelList[i] / 100) * (1 + irrs[i])**(st.session_state.yearWealth / 12)
    return initialInvInterest

def displayReturns():
    irrs = [0.02, 0.05, 0.1]
    with st.form("returnsForm"):
        st.title("Expected return")
        spaces(2)
        col1, col2, col3, col4, col5 = st.columns([3,0.2,3,0.2,3])
        now = datetime.datetime.now()
        with col1:
            st.markdown(f"<p class='subTitle'>Summary - {now.strftime("%b %Y")}</p>", unsafe_allow_html=True)
            col11, col22, col33 = st.columns([3.4, 0.2, 4])
            with col11:
                st.markdown(f"<p class='nameRe'>Initial investment</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Monthly saving</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Investment term</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameRe'>Invested savings</p>", unsafe_allow_html=True)
            with col22:
                st.markdown(f"<p class='twoPointsRe'>:</p>", unsafe_allow_html=True)
                for i in range(2):
                    st.markdown(f"<p class='twoPoints'>:</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='twoPointsRe'>:</p>", unsafe_allow_html=True)
            with col33:
                initialInvestment = "{:,.0f}".format(st.session_state.investment)
                st.markdown(f"<p class='valueRe'>CHF {initialInvestment}</p>", unsafe_allow_html=True)
                monthlySaving = "{:,.0f}".format(st.session_state.monthly)
                st.markdown(f"<p class='value'>CHF {monthlySaving}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='value'>{st.session_state.yearWealth} months</p>", unsafe_allow_html=True)
                totInvestedSaving = "{:,.0f}".format(st.session_state.monthly * st.session_state.yearWealth)
                st.markdown(f"<p class='valueRe'>CHF {totInvestedSaving}</p>", unsafe_allow_html=True)
        with col2:
            st.write("->")
        with col3:
            st.markdown(f"<p class='subTitle'>Average return rate</p>", unsafe_allow_html=True)
            returnRateInitialInvestment = ((initialInvInterestPartialFun(irrs) / st.session_state.investment)
                            ** (1 / (st.session_state.yearWealth / 12)) - 1)
            monthly_rate = npf.rate(nper=st.session_state.yearWealth, pmt=(st.session_state.monthly * -1), pv=0, fv=futureValueFun(irrs), when='end')
            annual_rate = (1 + monthly_rate) ** 12 - 1
            finalValueuno = ((returnRateInitialInvestment * st.session_state.investment / st.session_state.yearWealth) 
            + (annual_rate * st.session_state.monthly)) / ((st.session_state.investment / st.session_state.yearWealth) + st.session_state.monthly)
            st.markdown(f"<p class='percent'>{"{:,.2f}".format((finalValueuno * 100))}%</p>", unsafe_allow_html=True)
        with col4:
            st.write("->")
        with col5:
            st.markdown(f"<p class='subTitle'>Expected value - {(now + relativedelta(months=st.session_state.yearWealth)).strftime("%b %Y")}</p>", unsafe_allow_html=True)
            col111, col222, col333 = st.columns([3.4, 0.2, 4])
            with col111:
                st.markdown(f"<p class='name'>Initial inv. interest</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='name'>Saving interest</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameGr'>Total interest</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='nameGr'>Total value</p>", unsafe_allow_html=True)
            with col222:
                for i in range(2):
                    st.markdown(f"<p class='twoPoints'>:</p>", unsafe_allow_html=True)
                for i in range(2):
                    st.markdown(f"<p class='twoPointsGr'>:</p>", unsafe_allow_html=True)
            with col333:
                initialInvInterest = initialInvInterestPartialFun(irrs) - st.session_state.investment
                st.markdown(f"<p class='value'>CHF {"{:,.2f}".format(initialInvInterest)}</p>", unsafe_allow_html=True)
                savingInterest = futureValueFun(irrs) - st.session_state.monthly * st.session_state.yearWealth
                st.markdown(f"<p class='value'>CHF {"{:,.2f}".format(savingInterest)}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='valueGr'>CHF {"{:,.2f}".format(savingInterest + initialInvInterest)}</p>", unsafe_allow_html=True)
                st.markdown(f"<p class='valueGr'>CHF {"{:,.2f}".format(savingInterest + initialInvInterest + (st.session_state.monthly * st.session_state.yearWealth) + st.session_state.investment)}</p>", unsafe_allow_html=True)
                
        spaces(2)
        previous = st.form_submit_button("Previous")
        if previous:
            return {
                "next": False
            }