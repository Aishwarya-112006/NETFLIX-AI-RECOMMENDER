import streamlit as st
from utils_1 import set_background
from components.sidebar import show_sidebar

# ==========================================
# Page Configuration
# ==========================================

st.set_page_config(
    page_title="About",
    page_icon="ℹ️",
    layout="wide"
)

set_background("assets/netflix_bg.jpg")
show_sidebar()

# ==========================================
# Header
# ==========================================

st.markdown("""
<h1 style='text-align:center;
font-size:55px;
font-weight:900;
color:white;'>

🎬 About This Project

</h1>
""", unsafe_allow_html=True)

st.markdown("---")

# ==========================================
# Project Overview
# ==========================================

st.subheader("📌 Project Overview")

st.write("""
The **Netflix Recommendation System** is an AI-powered web application that recommends movies and TV shows using **Content-Based Filtering**.

It analyzes movie descriptions and metadata to suggest titles that are similar to the one selected by the user.

The application also integrates with the **TMDB API** to fetch real-time movie posters, ratings, and release information.
""")

st.markdown("---")

# ==========================================
# Machine Learning Workflow
# ==========================================

st.subheader("🤖 Machine Learning Workflow")

st.markdown("""
1. Load Netflix Dataset

2. Clean the Dataset

3. Feature Engineering

4. TF-IDF Vectorization

5. Cosine Similarity

6. Recommend Similar Movies

7. Fetch Posters using TMDB API

8. Display Results in Streamlit
""")

st.markdown("---")

# ==========================================
# Tech Stack
# ==========================================

st.subheader("💻 Tech Stack")

col1, col2 = st.columns(2)

with col1:

    st.success("Python")

    st.success("Pandas")

    st.success("NumPy")

    st.success("Scikit-Learn")

    st.success("Pickle")

with col2:

    st.success("Streamlit")

    st.success("TMDB API")

    st.success("Plotly")

    st.success("HTML/CSS")

    st.success("Git & GitHub")

st.markdown("---")

# ==========================================
# Features
# ==========================================

st.subheader("✨ Features")

st.markdown("""
✅ AI Movie Recommendation

✅ Netflix Dashboard

✅ Interactive Analytics

✅ Movie Posters

✅ Search Functionality

✅ Content-Based Recommendation

✅ Responsive Netflix UI

✅ TMDB Integration
""")

st.markdown("---")

# ==========================================
# Developer
# ==========================================

st.subheader("👩‍💻 Developer")

st.markdown("""
### Aishwarya Singh

B.Tech Computer Science Engineering

IILM University, Greater Noida

Passionate about

- Artificial Intelligence
- Machine Learning
- Data Science
- Full Stack Development
""")

st.markdown("---")

# ==========================================
# Contact
# ==========================================

st.subheader("🔗 Connect With Me")

st.markdown("""
📧 Email: aishwary1098@gmail.com

💼 LinkedIn:
https://www.linkedin.com/in/aishwarya-singh-112006

💻 GitHub:
https://github.com/Aishwarya-112006
""")

st.markdown("---")

st.markdown(
"""
<div style='text-align:center;color:white;'>

Made with ❤️ using Python, Streamlit and Machine Learning.

</div>
""",
unsafe_allow_html=True
) 