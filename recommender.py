import pandas as pd
import pickle

from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Load dataset
movies = pd.read_csv("data/netflix_cleaned.csv")

# Fill missing values
features = [
    "title",
    "director",
    "cast",
    "country",
    "listed_in",
    "description"
]

for feature in features:
    movies[feature] = movies[feature].fillna("")

# Create one combined text column
movies["combined_features"] = (
    movies["title"] + " " +
    movies["director"] + " " +
    movies["cast"] + " " +
    movies["country"] + " " +
    movies["listed_in"] + " " +
    movies["description"]
)

# Convert text into vectors
cv = CountVectorizer(stop_words="english", max_features=5000)

vectors = cv.fit_transform(movies["combined_features"]).toarray()

# Calculate cosine similarity
similarity = cosine_similarity(vectors)

# Save pickle files
pickle.dump(movies, open("movie_list.pkl", "wb"))
pickle.dump(similarity, open("similarity.pkl", "wb"))

print("movie_list.pkl created!")
print("similarity.pkl created!")