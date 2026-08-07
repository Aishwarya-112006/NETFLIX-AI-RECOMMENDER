import base64
import streamlit as st

def set_background(image_file):
    with open(image_file, "rb") as img:
        encoded = base64.b64encode(img.read()).decode()

    css = f"""
    <style>

    .stApp {{
        background: linear-gradient(
            rgba(0,0,0,0.65),
            rgba(0,0,0,0.85)
        ),
        url("data:image/jpg;base64,{encoded}");

        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}

    [data-testid="stSidebar"] {{
        background-color: rgba(0,0,0,0.88);
    }}

    </style>
    """

    st.markdown(css, unsafe_allow_html=True)