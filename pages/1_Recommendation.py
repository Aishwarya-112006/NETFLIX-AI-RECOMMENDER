import streamlit as st
import pickle
import requests

from utils import load_css
from utils_1 import set_background

# =====================================================
# Page Configuration
# =====================================================

st.set_page_config(
    page_title="Netflix Recommendation",
    page_icon="🎬",
    layout="wide"
)

load_css()
set_background("assets/netflix_bg.jpg")

# =====================================================
# Watchlist Session
# =====================================================

if "watchlist" not in st.session_state:
    st.session_state.watchlist = []

# =====================================================
# Title
# =====================================================

st.title("🎬 Netflix Movie Recommendation System")

st.write(
    "Select a movie or TV show and get AI-powered recommendations."
)

st.markdown("---")

# =====================================================
# Load Pickle Files
# =====================================================

movies = pickle.load(open("movie_list.pkl", "rb"))
similarity = pickle.load(open("similarity.pkl", "rb"))
# =====================================================
# Filters
# =====================================================

st.markdown("## 🎯 Filter Movies")

col1, col2 = st.columns(2)

with col1:

    search = st.text_input(
        "🔍 Search Movie",
        placeholder="Enter movie name..."
    )

with col2:

    sort_option = st.selectbox(
        "Sort",
        [
            "A-Z",
            "Z-A"
        ]
    )

# =====================================================
# TMDB API
# =====================================================

API_KEY = "5a096566c02cbaa2c2cfbab5cc7bef38"

# Example:
# API_KEY = "123456789abcdef"

# =====================================================
# Fetch Poster
# =====================================================
def fetch_movie_details(movie_name):

    try:

        search_url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={API_KEY}"
            f"&query={movie_name}"
        )

        response = requests.get(search_url, timeout=10)

        if response.status_code != 200:
            return None

        results = response.json()["results"]

        if len(results) == 0:
            return None

        movie_id = results[0]["id"]

        detail_url = (
            f"https://api.themoviedb.org/3/movie/"
            f"{movie_id}"
            f"?api_key={API_KEY}"
        )

        detail = requests.get(detail_url).json()

        poster = None

        if detail.get("poster_path"):

            poster = (
                "https://image.tmdb.org/t/p/w500"
                + detail["poster_path"]
            )

        genres = ", ".join(
            [g["name"] for g in detail["genres"]]
        )

        return {

            "poster": poster,

            "title": detail["title"],

            "rating": detail["vote_average"],

            "release": detail["release_date"],

            "runtime": detail["runtime"],

            "genres": genres,

            "overview": detail["overview"]

        }

    except:

        return None

# =====================================================
# Fetch Trailer
# =====================================================

def fetch_trailer(movie_name):

    try:

        url = (
            f"https://api.themoviedb.org/3/search/movie"
            f"?api_key={API_KEY}"
            f"&query={movie_name}"
        )

        response = requests.get(url)

        data = response.json()

        if len(data["results"]) == 0:
            return None

        movie_id = data["results"][0]["id"]

        url = (
            f"https://api.themoviedb.org/3/movie/"
            f"{movie_id}/videos"
            f"?api_key={API_KEY}"
        )

        response = requests.get(url)

        videos = response.json()["results"]

        for video in videos:

            if (
                video["site"] == "YouTube"
                and video["type"] == "Trailer"
            ):

                return (
                    "https://www.youtube.com/watch?v="
                    + video["key"]
                )

    except:
        pass

    return None

# =====================================================
# Recommendation Function
# =====================================================

def recommend(movie):

    index = movies[movies["title"] == movie].index[0]

    distances = similarity[index]

    movie_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]

    recommended_movies = []
    recommended_details = []

    for i in movie_list:

        movie_title = movies.iloc[i[0]].title

        recommended_movies.append(movie_title)

        recommended_details.append(fetch_movie_details(movie_title))

    return recommended_movies, recommended_details

st.markdown("---")

st.subheader("🎬 Movie Details Explorer")

movie_name = st.selectbox(

    "Choose any movie",

    movies["title"].values,

    key="details"

)

details = fetch_movie_details(movie_name)

if details:

    col1, col2 = st.columns([1,2])

    with col1:

        st.image(
            details["poster"],
            use_container_width=True
        )

    with col2:

        st.markdown(f"# {details['title']}")

        st.write(
            f"⭐ Rating: {details['rating']}"
        )

        st.write(
            f"📅 Release: {details['release']}"
        )

        st.write(
            f"⏱ Runtime: {details['runtime']} min"
        )

        st.write(
            f"🎭 Genres: {details['genres']}"
        )

        st.write(details["overview"])

        trailer = fetch_trailer(movie_name)

        if trailer:

            st.link_button(
                "▶ Watch Trailer",
                trailer,
                use_container_width=True
            )

        else:

            st.info("Trailer not available.")

# =====================================================
# Movie Dropdown
# =====================================================

movie_list = movies["title"].tolist()

if search:

    movie_list = [
        movie for movie in movie_list
        if search.lower() in movie.lower()
    ]

if sort_option == "A-Z":
    movie_list = sorted(movie_list)

else:
    movie_list = sorted(movie_list, reverse=True)

selected_movie = st.selectbox(
    "🎥 Choose a Movie",
    movie_list
)
st.info(f"🎬 {len(movie_list)} movies available")

# =====================================================
# Recommend Button
# =====================================================

if st.button("🍿 Recommend Movies", use_container_width=True):

    names, details = recommend(selected_movie)

    st.markdown("## 🎬 Recommended For You")

    cols = st.columns(5)

    for idx in range(5):

        with cols[idx]:

            movie = details[idx]

            if movie and movie["poster"]:
                st.image(movie["poster"], use_container_width=True)
            else:
                st.image(
                    "https://via.placeholder.com/300x450?text=No+Poster",
                    use_container_width=True
                )

            st.markdown(
                f"""
                <div class="movie-card">

                <div class="movie-title">

                {names[idx]}

                </div>

                """,
                unsafe_allow_html=True
            )

            if movie:

                st.write(f"⭐ Rating: {movie['rating']}")

                st.write(f"📅 Year: {movie['release']}")

                st.caption(movie["overview"][:140] + "...")

                trailer = fetch_trailer(names[idx])

                if trailer:

                    st.link_button(
                        "▶️ Watch Trailer",
                        trailer,
                        use_container_width=True
                    )

                else:

                    st.button(
                        "Trailer Not Available",
                        disabled=True,
                        key=f"disabled_{idx}"
                    )

            if st.button("➕ Add to Watchlist", key=f"watch_{idx}"):

                if names[idx] not in st.session_state.watchlist:

                    st.session_state.watchlist.append(names[idx])

                    st.success("Added!")

                else:

                    st.info("Already Added")
            st.markdown(
                "</div>",
                unsafe_allow_html=True
            )

# =====================================================
# Watchlist
# =====================================================

st.markdown("---")

st.subheader("⭐ My Watchlist")

if len(st.session_state.watchlist) == 0:

    st.info("Your watchlist is empty.")

else:

    for movie in st.session_state.watchlist:

        st.write("🎬", movie)

# =====================================================
# Clear Watchlist
# =====================================================

if st.button("🗑 Clear Watchlist"):

    st.session_state.watchlist = []

    st.rerun()

# =====================================================
# Footer
# =====================================================

st.markdown("---")

st.markdown(
    """
<div style='text-align:center'>

### ❤️ Developed by Aishwarya Singh

Netflix AI Recommendation System

Python • Streamlit • Scikit-Learn • TMDB API

</div>
""",
    unsafe_allow_html=True
)