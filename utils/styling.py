import streamlit as st
import base64

# convert a image in a stream of bite in base 64.
def load_image_as_base64(image_path):
    with open(image_path, "rb") as img_file:
        return base64.b64encode(img_file.read()).decode()
    
# custom styling for most of the pages, for visual aspects (e.g. colors, background-colors, text-align, text-size, text-style..).
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
                font-size: 18px;
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
            button:focus {
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
            div[data-testid="stForm"] {
                border: None;
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

# custom styling for the dashboard interface page (not the dashboard specifically, but the page where the dashboard is)
def custom_stylingDashboard():
    apply_custom_styling()
    st.markdown(
        """
        <style>
            div[data-testid="stForm"] {
                border: 2px solid #110F37;
            }
            div[data-testid="stSidebarContent"] div[data-testid="stForm"] {
                border: None
            }
            div[data-testid="stSidebarContent"] button[kind="secondaryFormSubmit"]:focus {
                background-color: #7f94f0 !important;
                border: none;
            }
            body button[kind="secondaryFormSubmit"] {
                background-color: #110F37 !important;
                width: 100%;
            }
            body button[kind="secondaryFormSubmit"]:focus {
                background-color: #7f94f0 !important;
            }
            body button[kind="secondaryFormSubmit"] p {
                color: #F1EEE5 !important;
                font-weight: bold !important;
            }
            div[data-testid="stSidebarContent"] button[kind="secondaryFormSubmit"] {
                background-color: #F1EEE5 !important;
            }
            div[data-testid="stSidebarContent"] button[kind="secondaryFormSubmit"] p {
                color: #110F37 !important;
            }
            h2[class='navigation'] {
                font-weight: bold !important;
                font-style: normal !important;
                font-size: 2.4em !important;
            }
            h2[class='assets'] {
                font-style: normal !important;
                font-size: 2.4em !important;
                text-align:center;
                margin-top: -20px;
            }
            div[data-testid="stForm"] {
                margin-top:-60px;
            }
            div[data-testid="stSidebarContent"] div[data-testid="stForm"] {
                margin-top:-60px;
            }

        </style>
        """,
        unsafe_allow_html=True
    )

# custom styling for the output interface (the entirety of the last page).
def custom_stylingReturn():
        apply_custom_styling()
        st.markdown(
        """
        <style>
            div[data-testid="stForm"] {
                background-color: #375A6A !important;
            }
            div[data-testid="stForm"] * {
                color: #DCD7CD !important;
            }
            div[data-testid="stForm"] button p, button span {
                color: #110F37 !important;
            }
            h1 {
                font-size: 3em !important;
            }
            p[class='subTitle'] {
                text-align: center;
                font-size: 1.6em !important;
                font-weight: bold !important;
            }
            p[class='subTitleM'] {
                text-align: right;
                font-size: 1.6em !important;
                font-weight: bold !important;
            }
            p[class='name'], p[class='nameGr'], p[class='nameG'] {
                font-weight: bold !important;
            }
            p[class='name'], p[class='nameGr'], p[class='nameRe'], p[class='nameG'], p[class='twoPoints'], p[class='twoPointsGr'], p[class='twoPointsRe'],
                    p[class='twoPointsG'], p[class='value'], p[class='valueGr'], p[class='valueRe'], p[class='valueG'] {
                margin-bottom: 0;
                text-align: center;
            }
            p[class='nameGr'], p[class='valueGr'], p[class='twoPointsGr'] {
                color: #05f742 !important;
                font-weight: bold !important;
            }
            p[class='nameRe'], p[class='valueRe'], p[class='twoPointsRe'] {
                color: #f78307 !important;
                font-weight: bold !important;
            }
            p[class='percent'] {
                font-size: 2.7em !important;
                font-weight: bold !important;
                text-align: center;
            }
            p[class='nameG'], p[class='twoPointsG'], p[class='valueG'] {
                font-size: 1.2em !important;
            }
        </style>
        """,
        unsafe_allow_html=True
    )
