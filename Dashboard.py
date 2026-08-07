import requests
import streamlit as st
import pandas as pd
import plotly.express as px

from utils_1 import set_background
from components.sidebar import show_sidebar

# -------------------------------------------------------
# Page Configuration
# -------------------------------------------------------

st.set_page_config(
    page_title="Netflix Recommendation System",
    page_icon="🎬",
    layout="wide"
)

# -------------------------------------------------------
# Background
# -------------------------------------------------------

set_background("assets/netflix_bg.jpg")
show_sidebar()
# -------------------------------------------------------
# TMDB Featured Movie
# -------------------------------------------------------

from requests.exceptions import RequestException

API_KEY = "5a096566c02cbaa2c2cfbab5cc7bef38"

# -------------------------------------------------------
# Get Featured Movie
# -------------------------------------------------------

def get_featured_movie(movie_name):

    url = (
        f"https://api.themoviedb.org/3/search/tv"
        f"?api_key={API_KEY}"
        f"&query={movie_name}"
    )

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        if not data.get("results"):
            return None

        movie = data["results"][0]

        poster = None

        if movie.get("poster_path"):

            poster = (
                "https://image.tmdb.org/t/p/w500"
                + movie["poster_path"]
            )

        return {
            "title": movie.get("name", "Unknown"),
            "overview": movie.get(
                "overview",
                "No overview available."
            ),
            "rating": movie.get(
                "vote_average",
                "N/A"
            ),
            "poster": poster,
            "year": movie.get(
                "first_air_date",
                ""
            )[:4]
        }

    except RequestException:

        return None
# -------------------------------------------------------
# Get Trending Movies
# -------------------------------------------------------

def get_trending_movies():

    url = (
        f"https://api.themoviedb.org/3/trending/movie/week"
        f"?api_key={API_KEY}"
    )

    try:

        response = requests.get(url, timeout=10)

        response.raise_for_status()

        data = response.json()

        movies = []

        for movie in data.get("results", [])[:5]:

            poster = None

            if movie.get("poster_path"):

                poster = (
                    "https://image.tmdb.org/t/p/w500"
                    + movie["poster_path"]
                )

            else:

                poster = (
                    "https://via.placeholder.com/"
                    "300x450?text=No+Poster"
                )

            movies.append({

                "title": movie.get("title", "Unknown"),

                "poster": poster,

                "rating": movie.get("vote_average", "N/A"),

                "year": movie.get("release_date", "")[:4]

            })

        return movies

    except RequestException:

        return []


    
        
# -------------------------------------------------------
# Load CSS
# -------------------------------------------------------

def load_css():

    try:

        with open("styles/style.css", encoding="utf-8") as css:

            st.markdown(

                f"<style>{css.read()}</style>",

                unsafe_allow_html=True

            )

    except FileNotFoundError:

        st.warning("style.css not found.")

load_css()
# -------------------------------------------------------
# Load Dataset
# -------------------------------------------------------

try:

    df = pd.read_csv("data/netflix_titles.csv")

except FileNotFoundError:

    st.error("❌ netflix_titles.csv not found.")

    st.stop()

except Exception as e:

    st.error(f"Error loading dataset: {e}")

    st.stop()

# -------------------------------------------------------
# Hero Section
# -------------------------------------------------------

st.markdown(
    """
    <div style="
        padding:40px 20px;
        border-radius:20px;
        background:rgba(0,0,0,0.55);
        margin-bottom:20px;
    ">

    <h1 style="
        font-size:64px;
        font-weight:900;
        color:#E50914;
        margin-bottom:10px;
    ">

    🎬 NETFLIX AI RECOMMENDER

    </h1>

    <p style="
        font-size:22px;
        color:white;
        line-height:1.8;
        max-width:900px;
    ">

    Discover movies and TV shows with an AI-powered recommendation engine.
    Explore trending titles, view analytics, and find your next favorite
    movie using Machine Learning and the TMDB API.

    </p>

    </div>
    """,
    unsafe_allow_html=True
)
# -------------------------------------------------------
# Quick Stats
# -------------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🎬 Total Titles", len(df))

with col2:
    st.metric("🎥 Movies", len(df[df["type"] == "Movie"]))

with col3:
    st.metric("📺 TV Shows", len(df[df["type"] == "TV Show"]))
# -------------------------------------------------------
# Featured Movie
# -------------------------------------------------------

# -------------------------------------------------------
# Featured Movie
# -------------------------------------------------------

st.markdown("---")
st.subheader("🌟 Featured Today")

featured = get_featured_movie("Stranger Things")

if featured:

    col1, col2 = st.columns([1, 2], gap="large")

    with col1:

        if featured["poster"]:

            st.image(
                featured["poster"],
                use_container_width=True
            )

        else:

            st.info("Poster not available.")

    with col2:

        st.markdown(
            f"""
            <h2 style="color:white;">
            {featured['title']}
            </h2>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            f"⭐ **TMDB Rating:** {featured['rating']}"
        )

        st.markdown(
            f"📅 **Release Year:** {featured['year']}"
        )

        st.markdown("### 📖 Overview")

        st.write(featured["overview"])

        st.markdown("")

        if st.button(
            "🎬 Get Similar Recommendations",
            use_container_width=True
        ):

            st.switch_page("pages/1_Recommendation.py")

else:

    st.warning(
        "Unable to load featured movie. Please try again later."
    )


# -------------------------------------------------------
# Trending Movies
# -------------------------------------------------------

st.markdown("---")
st.subheader("🔥 Trending Movies This Week")

movie_posters = get_trending_movies()

if movie_posters:

    cols = st.columns(5)

    for col, movie in zip(cols, movie_posters):

        with col:

            st.image(
                movie["poster"],
                use_container_width=True
            )

            st.markdown(
                f"""
                <h4 style="
                color:white;
                text-align:center;
                margin-top:10px;
                ">
                {movie['title']}
                </h4>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <p style="
                color:#dddddd;
                text-align:center;
                ">
                ⭐ {movie['rating']}
                </p>
                """,
                unsafe_allow_html=True
            )

            st.markdown(
                f"""
                <p style="
                color:#bbbbbb;
                text-align:center;
                ">
                📅 {movie['year']}
                </p>
                """,
                unsafe_allow_html=True
            )

else:

    st.info("Trending movies are currently unavailable.")

# -------------------------------------------------------
# Live Trending Movies
# -------------------------------------------------------

movie_posters = get_trending_movies()




# -------------------------------------------------------
# Netflix Statistics
# -------------------------------------------------------

st.markdown("---")

st.subheader("📊 Netflix Statistics")

total_titles = len(df)
movies_count = len(df[df["type"] == "Movie"])
tvshows_count = len(df[df["type"] == "TV Show"])
countries = (
    df["country"]
    .fillna("")
    .str.split(", ")
    .explode()
    .nunique()
)

col1, col2, col3, col4 = st.columns(4)

with col1:

    st.metric(
        "🎬 Total Titles",
        total_titles
    )

with col2:

    st.metric(
        "🎥 Movies",
        movies_count
    )

with col3:

    st.metric(
        "📺 TV Shows",
        tvshows_count
    )

with col4:

    st.metric(
        "🌍 Countries",
        countries
    )


# -------------------------------------------------------
# Dataset Insights
# -------------------------------------------------------

st.markdown("---")

col1, col2 = st.columns(2)

with col1:

    st.info(
        f"""
**Oldest Release Year**

{df['release_year'].min()}
"""
    )

with col2:

    st.info(
        f"""
**Latest Release Year**

{df['release_year'].max()}
"""
    )

# -------------------------------------------------------
# Popular Genres
# -------------------------------------------------------

st.markdown("---")

st.subheader("🎭 Top 10 Netflix Genres")

genres = (
    df["listed_in"]
    .dropna()
    .str.split(", ")
    .explode()
)

genre_count = (
    genres.value_counts()
    .head(10)
    .reset_index()
)

genre_count.columns = [
    "Genre",
    "Count"
]

fig = px.bar(
    genre_count,
    x="Count",
    y="Genre",
    orientation="h",
    text="Count",
    title="Most Popular Genres",
    height=500
)

fig.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font_color="white",

    title_font_size=22,

    yaxis_title="",

    xaxis_title="Number of Titles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Release Year Timeline
# -------------------------------------------------------

st.markdown("---")

st.subheader("📈 Netflix Content Growth Over Time")

year_data = (
    df["release_year"]
    .value_counts()
    .sort_index()
    .reset_index()
)

year_data.columns = [
    "Release Year",
    "Titles"
]

fig = px.line(
    year_data,
    x="Release Year",
    y="Titles",
    markers=True,
    title="Netflix Titles Released Per Year"
)

fig.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font_color="white",

    title_font_size=22,

    xaxis_title="Release Year",

    yaxis_title="Number of Titles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Top 10 Countries
# -------------------------------------------------------

st.markdown("---")

st.subheader("🌍 Top 10 Content Producing Countries")

country_data = (
    df["country"]
    .fillna("Unknown")
    .str.split(", ")
    .explode()
)

country_count = (
    country_data
    .value_counts()
    .head(10)
    .reset_index()
)

country_count.columns = [
    "Country",
    "Titles"
]

fig = px.bar(
    country_count,
    x="Country",
    y="Titles",
    color="Titles",
    text="Titles",
    title="Top 10 Countries by Netflix Titles"
)

fig.update_layout(

    paper_bgcolor="rgba(0,0,0,0)",

    plot_bgcolor="rgba(0,0,0,0)",

    font_color="white",

    title_font_size=22,

    xaxis_title="Country",

    yaxis_title="Number of Titles"
)

st.plotly_chart(
    fig,
    use_container_width=True
)

# -------------------------------------------------------
# Search & Filter Dashboard
# -------------------------------------------------------

st.markdown("---")
st.subheader("🔍 Search Netflix Library")

col1, col2, col3 = st.columns(3)

with col1:

    search = st.text_input(
        "Search Title"
    )

with col2:

    selected_type = st.selectbox(
        "Content Type",
        ["All", "Movie", "TV Show"]
    )

with col3:

    years = sorted(
        df["release_year"].unique(),
        reverse=True
    )

    selected_year = st.selectbox(
        "Release Year",
        ["All"] + list(years)
    )


# -------------------------------------------------------
# Apply Filters
# -------------------------------------------------------

filtered_df = df.copy()

if search:

    filtered_df = filtered_df[
        filtered_df["title"]
        .str.contains(
            search,
            case=False,
            na=False
        )
    ]

if selected_type != "All":

    filtered_df = filtered_df[
        filtered_df["type"] == selected_type
    ]

if selected_year != "All":

    filtered_df = filtered_df[
        filtered_df["release_year"] == selected_year
    ]

st.success(
    f"Found {len(filtered_df)} titles."
)

st.dataframe(

    filtered_df[
        [
            "title",
            "type",
            "release_year",
            "country",
            "listed_in"
        ]
    ],

    use_container_width=True,

    height=400
)

# -------------------------------------------------------
# Features
# -------------------------------------------------------

st.markdown("---")

st.subheader("🚀 Features")

feature1, feature2, feature3 = st.columns(3)

with feature1:

    st.info("""
🎯 AI Recommendation

Get similar movies using
Machine Learning.
""")

with feature2:

    st.info("""
📊 Analytics Dashboard

Explore Netflix data with
interactive charts.
""")

with feature3:

    st.info("""
🎬 TMDB Integration

Movie Posters,
Ratings &
Overview.
""")

# -------------------------------------------------------
# Footer
# -------------------------------------------------------

st.markdown("---")

st.markdown(
    """
<div style="text-align:center;color:white;">

### ❤️ Developed by Aishwarya Singh

B.Tech CSE Student

Built using

Python • Pandas • Scikit-Learn • Streamlit • TMDB API

</div>
""",
    unsafe_allow_html=True,
)