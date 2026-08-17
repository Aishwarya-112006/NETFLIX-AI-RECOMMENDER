import os
import pickle
import streamlit as st
import requests


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title="Netflix Recommendation",
    page_icon="🎬",
    layout="wide"
)


# ============================================================
# PATH CONFIGURATION
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MOVIE_LIST_PATH = os.path.join(BASE_DIR, "movie_list.pkl")
SIMILARITY_PATH = os.path.join(BASE_DIR, "similarity.pkl")


# ============================================================
# DOWNLOAD MODEL FILES IF NOT PRESENT
# ============================================================

def ensure_models():
    """
    Download movie_list.pkl and similarity.pkl from Google Drive
    if they are not already present.
    """

    if os.path.exists(MOVIE_LIST_PATH) and os.path.exists(SIMILARITY_PATH):
        return

    try:
        from download_models import download_models

        with st.spinner("Downloading recommendation models..."):
            download_models()

    except Exception as e:
        st.error("Unable to download recommendation models.")
        st.error(str(e))
        st.stop()


# ============================================================
# LOAD MODELS
# ============================================================

@st.cache_resource
def load_models():

    ensure_models()

    if not os.path.exists(MOVIE_LIST_PATH):
        st.error("movie_list.pkl was not found.")
        st.stop()

    if not os.path.exists(SIMILARITY_PATH):
        st.error("similarity.pkl was not found.")
        st.stop()

    try:
        with open(MOVIE_LIST_PATH, "rb") as file:
            movies = pickle.load(file)

        with open(SIMILARITY_PATH, "rb") as file:
            similarity = pickle.load(file)

        return movies, similarity

    except Exception as e:
        st.error("Error while loading recommendation models.")
        st.error(str(e))
        st.stop()


movies, similarity = load_models()


# ============================================================
# TMDB API
# ============================================================

def fetch_poster(movie_id):

    try:

        url = f"https://api.themoviedb.org/3/movie/{movie_id}"

        params = {
            "api_key": st.secrets["TMDB_API_KEY"],
            "language": "en-US"
        }

        response = requests.get(
            url,
            params=params,
            timeout=10
        )

        data = response.json()

        poster_path = data.get("poster_path")

        if poster_path:
            return "https://image.tmdb.org/t/p/w500" + poster_path

    except Exception:
        pass

    return None


# ============================================================
# RECOMMENDATION FUNCTION
# ============================================================

def recommend(movie):

    try:

        # Find selected movie index
        movie_index = movies[movies["title"] == movie].index[0]

        # Get similarity scores
        distances = similarity[movie_index]

        # Sort movies according to similarity
        movie_list = sorted(
            list(enumerate(distances)),
            reverse=True,
            key=lambda x: x[1]
        )

        recommended_movies = []
        recommended_posters = []

        # Get top 5 recommendations
        for i in movie_list[1:6]:

            movie_index = i[0]

            title = movies.iloc[movie_index].title

            recommended_movies.append(title)

            # Try to get poster
            poster = None

            if "id" in movies.columns:
                poster = fetch_poster(
                    movies.iloc[movie_index]["id"]
                )

            elif "movie_id" in movies.columns:
                poster = fetch_poster(
                    movies.iloc[movie_index]["movie_id"]
                )

            recommended_posters.append(poster)

        return recommended_movies, recommended_posters

    except Exception as e:

        st.error("Unable to generate recommendations.")
        st.error(str(e))

        return [], []


# ============================================================
# PAGE TITLE
# ============================================================

st.markdown(
    """
    <h1 style="
        text-align:center;
        font-size:42px;
        margin-bottom:10px;
    ">
        🎬 Netflix Movie Recommendation System
    </h1>
    """,
    unsafe_allow_html=True
)

st.markdown(
    """
    <p style="
        text-align:center;
        font-size:18px;
        margin-bottom:35px;
    ">
        Select a movie or TV show and get AI-powered recommendations.
    </p>
    """,
    unsafe_allow_html=True
)


# ============================================================
# MOVIE SELECTION
# ============================================================

if "title" not in movies.columns:

    st.error(
        "The movie_list.pkl file does not contain a 'title' column."
    )
    st.stop()


movie_titles = movies["title"].values


selected_movie = st.selectbox(
    "🎥 Select a movie or TV show",
    movie_titles
)


# ============================================================
# RECOMMEND BUTTON
# ============================================================

if st.button(
    "✨ Get Recommendations",
    use_container_width=True
):

    with st.spinner("Finding movies similar to your selection..."):

        names, posters = recommend(selected_movie)

    if names:

        st.markdown(
            f"## 🎯 Recommended Movies for **{selected_movie}**"
        )

        # Create five columns
        cols = st.columns(5)

        for col, name, poster in zip(
            cols,
            names,
            posters
        ):

            with col:

                if poster:

                    st.image(
                        poster,
                        use_container_width=True
                    )

                else:

                    st.markdown(
                        """
                        <div style="
                            height:250px;
                            display:flex;
                            align-items:center;
                            justify-content:center;
                            background:#222;
                            border-radius:10px;
                            font-size:50px;
                        ">
                        🎬
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                st.markdown(
                    f"""
                    <p style="
                        text-align:center;
                        font-weight:bold;
                        margin-top:10px;
                    ">
                        {name}
                    </p>
                    """,
                    unsafe_allow_html=True
                )


# ============================================================
# INFORMATION SECTION
# ============================================================

st.markdown("---")

st.markdown(
    """
    ### 🤖 How does it work?

    This recommendation system uses **Content-Based Filtering**
    and **Cosine Similarity** to identify movies and TV shows
    that are similar to the selected title.

    The system analyzes information such as:

    - 🎭 Genres
    - 🎬 Cast
    - ✍️ Description
    - 🎥 Director
    - 🌍 Country
    - ⭐ Other movie metadata

    The five most similar titles are then displayed as
    recommendations.
    """
)