import streamlit as st
import pandas as pd
import plotly.express as px
from utils_1 import set_background
from components.sidebar import show_sidebar

# ==========================================================
# Page Configuration
# ==========================================================

st.set_page_config(
    page_title="Netflix Analytics",
    page_icon="📊",
    layout="wide"
)

set_background("assets/netflix_bg.jpg")
show_sidebar()

# ==========================================================
# Load Dataset
# ==========================================================

df = pd.read_csv("data/netflix_titles.csv")

# ==========================================================
# Custom CSS
# ==========================================================

st.markdown("""
<style>

.big-title{
    text-align:center;
    color:white;
    font-size:52px;
    font-weight:900;
}

.subtitle{
    text-align:center;
    color:#dddddd;
    font-size:20px;
    margin-bottom:25px;
}

</style>
""", unsafe_allow_html=True)

# ==========================================================
# Header
# ==========================================================

st.markdown(
    "<h1 class='big-title'>📊 Netflix Analytics Dashboard</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle'>Explore Netflix's library with interactive analytics and insights.</p>",
    unsafe_allow_html=True
)

# ==========================================================
# KPI Cards
# ==========================================================

total_titles = len(df)
movies = len(df[df["type"] == "Movie"])
tvshows = len(df[df["type"] == "TV Show"])
countries = (
    df["country"]
    .fillna("")
    .str.split(", ")
    .explode()
    .nunique()
)

genres = (
    df["listed_in"]
    .fillna("")
    .str.split(", ")
    .explode()
    .nunique()
)

years = df["release_year"].nunique()

c1, c2, c3 = st.columns(3)

c1.metric("🎬 Total Titles", f"{total_titles:,}")
c2.metric("🎥 Movies", f"{movies:,}")
c3.metric("📺 TV Shows", f"{tvshows:,}")

c4, c5, c6 = st.columns(3)

c4.metric("🌍 Countries", countries)
c5.metric("🎭 Genres", genres)
c6.metric("📅 Release Years", years)

st.markdown("---")

# ==========================================================
# Movies vs TV Shows
# ==========================================================

left, right = st.columns(2)

with left:

    type_count = df["type"].value_counts()

    fig = px.pie(
        values=type_count.values,
        names=type_count.index,
        hole=0.55,
        title="Movies vs TV Shows"
    )

    fig.update_layout(
        template="plotly_dark",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    year_count = (
        df["release_year"]
        .value_counts()
        .sort_index()
    )

    fig = px.line(
        x=year_count.index,
        y=year_count.values,
        title="Titles Released Per Year",
        markers=True
    )

    fig.update_layout(
        template="plotly_dark",
        xaxis_title="Year",
        yaxis_title="Titles",
        height=450
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# Top Genres
# ==========================================================

left, right = st.columns(2)

with left:

    genres = (
        df["listed_in"]
        .dropna()
        .str.split(", ")
        .explode()
    )

    genre_count = genres.value_counts().head(10)

    fig = px.bar(
        x=genre_count.values,
        y=genre_count.index,
        orientation="h",
        title="Top 10 Genres"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Titles",
        yaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)

with right:

    country = (
        df["country"]
        .fillna("Unknown")
        .str.split(", ")
        .explode()
    )

    country_count = country.value_counts().head(10)

    fig = px.bar(
        x=country_count.values,
        y=country_count.index,
        orientation="h",
        title="Top 10 Countries"
    )

    fig.update_layout(
        template="plotly_dark",
        height=500,
        xaxis_title="Titles",
        yaxis_title=""
    )

    st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# Rating Distribution
# ==========================================================

rating_count = df["rating"].fillna("Unknown").value_counts().head(10)

fig = px.bar(
    x=rating_count.index,
    y=rating_count.values,
    title="Content Ratings Distribution"
)

fig.update_layout(
    template="plotly_dark",
    height=500,
    xaxis_title="Rating",
    yaxis_title="Number of Titles"
)

st.plotly_chart(fig, use_container_width=True)

st.markdown("---")

# ==========================================================
# Search Dataset
# ==========================================================

st.subheader("🔍 Search Netflix Library")

search = st.text_input("Search by Title")

filtered = df.copy()

if search:
    filtered = filtered[
        filtered["title"].str.contains(
            search,
            case=False,
            na=False
        )
    ]

st.dataframe(
    filtered[
        [
            "title",
            "type",
            "country",
            "release_year",
            "rating"
        ]
    ],
    use_container_width=True,
    height=450
)

# ==========================================================
# Download CSV
# ==========================================================

csv = filtered.to_csv(index=False).encode("utf-8")

st.download_button(
    "📥 Download Filtered Dataset",
    csv,
    "filtered_netflix_data.csv",
    "text/csv"
)