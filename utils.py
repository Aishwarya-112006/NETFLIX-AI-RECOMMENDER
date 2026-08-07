import streamlit as st

def load_css():
    try:
        with open("styles/style.css") as f:
            st.markdown(
                f"<style>{f.read()}</style>",
                unsafe_allow_html=True
            )
    except FileNotFoundError:
        st.warning("CSS file not found.")