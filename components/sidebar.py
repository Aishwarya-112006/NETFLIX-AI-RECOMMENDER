import streamlit as st

def show_sidebar():

    with st.sidebar:

        # -------------------------------
        # Netflix Logo
        # -------------------------------

        st.image(
            "assets/netflix_logo.jpg",   # or .png
            use_container_width=True
        )

        st.markdown(
            """
            <h2 style="text-align:center;color:white;">
            Netflix AI
            </h2>

            <p style="text-align:center;color:#b3b3b3;">
            Recommendation System
            </p>
            """,
            unsafe_allow_html=True
        )

        st.markdown("---")

        # =====================================
        # ADD STEP 2 HERE
        # =====================================

        st.page_link(
            "Dashboard.py",
            label="🏠 Dashboard",
             
        )

        st.page_link(
            "pages/1_Recommendation.py",
            label="🎬 Recommendations",
            
        )

        st.page_link(
            "pages/2_Analytics.py",
            label="📊 Analytics",
            
        )

        st.page_link(
            "pages/3_About.py",
            label="ℹ️ About Project",
            
        )

        st.markdown("---")

        # Project Statistics
        st.markdown("### 📈 Project Stats")

        st.markdown("**Dataset**")
        st.caption("8,807 Titles")

        st.markdown("**ML Model**")
        st.caption("Cosine Similarity")

        st.markdown("**Accuracy**")
        st.caption("Content Based")

        st.markdown("---")

        st.markdown(
            """
            **Developed by**

            Aishwarya Singh

            B.Tech CSE
            """
        )