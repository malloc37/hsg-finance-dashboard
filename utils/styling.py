import streamlit as st

def apply_custom_styling():
    st.markdown(
        """
        <style>
        .css-18e3th9 { background-color: #37474f; color: white; }
        .css-1cpxqw2 { color: #ffca28; }
        .css-qbe2hs { color: white; }
        </style>
        """,
        unsafe_allow_html=True
    )