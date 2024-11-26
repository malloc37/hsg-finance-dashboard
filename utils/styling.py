import streamlit as st
import base64
def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()

def apply_custom_styling():
    image_path = "resources/logo.png"
    image_base64 = load_image_as_base64(image_path)
    st.markdown(
        """
        <style>
            .stApp {
                background-color: #F1EEE5 !important;
                color: #110F37 !important;
            }
            body {
                background-color: #F1EEE5;
            }
            * {
                color: #110F37 !important;
                font-family: 'EB Garamond', serif !important;
                font-size: 18px !important;
            }
            p {
                font-size: 18px !important;
            }
            input[type="number"][step="10"] {
                text-align: center;
            }
            h1 {
                text-align: center;
                font-style: italic;
                font-size: 2.5em !important;
            }
            input[type=number], button {
                background-color: #DCD7CD !important;
                border: none !important;
                font-size: 18px;
            }
            body button:focus {
                background-color: #7f94f0 !important;
            }
            div[data-baseweb="select"]>div {
                background-color: #DCD7CD;
                color: #110F37;
                border: none;
            }
            div[data-baseweb="popover"] li {
                background-color: #DCD7CD;
                color: #110F37;
                border: none;
            }
            div[data-baseweb="popover"] li:hover {
                background-color: #7f94f0;
                color: #110F37;
                border: none;
            }
            .stMultiSelect [data-baseweb="tag"] {
                background-color: #7f94f0 !important; 
            }
            span[data-baseweb="tag"] {
                color: #110F37;
                background-color: #7f94f0;
            }
            div[data-testid="stNumberInputContainer"] {
                border: none;
            }
            div[role="slider"] {
                background-color: #110F37 !important;
            }
            .header-text {
                position: absolute;
                left: -90px;
                color: red !important;
                width: 200%;
                background-color: #110F37 !important;
                padding-top: 0.7%;
                padding-bottom: 0.3%;
                padding-left: 8%;
                top: -110px;
            }
            
            .stAppHeader {
                background-color: rgba(0, 0, 0, 0.0) !important;
            }
            div[data-testid="stExpanderDetails"] p {
                font-size: 16px !important;
                bottom: 8%;
            }
            div[data-testid="stSidebarContent"] {
                background-color: #DCD7CD !important;
            }
            div[data-testid="stSidebarContent"] input[type=number], div[data-testid="stSidebarContent"] button {
                background-color: #F1EEE5 !important;
                border: none !important;
                font-size: 18px;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
    st.markdown(
        f"""
        <div class="header-text">
            <img src="data:image/png;base64,{image_base64}" alt="Logo" style="width: 170px; height: auto;">
        </div>
        """,
        unsafe_allow_html=True
    )

    