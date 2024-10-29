import streamlit as st
from components.input_form import display_input_form
from components.options_list import display_options_list
from components.dashboard import display_dashboard
from utils.styling import apply_custom_styling

st.set_page_config(page_title="Investment Advisor Dashboard", layout="wide")

# Apply custom styling
apply_custom_styling()

# Collect user input
user_input = display_input_form()

# Display options based on user input
if user_input:
    selected_option = display_options_list(user_input)

    # Show dashboard for selected option
    if selected_option:
        display_dashboard(selected_option)