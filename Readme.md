# 🎬 Netflix AI Recommendation System

An AI-powered **Netflix Movie & TV Show Recommendation System** built using **Python, Machine Learning, Streamlit, Pandas, Scikit-Learn, TMDB API, Docker, and Kubernetes**.

The system uses **Content-Based Filtering** and **Cosine Similarity** to recommend movies and TV shows similar to the title selected by the user.

---

## 🚀 Live Demo

🌐 **Live Application:**

https://netflix-ai-recommender-hrgjfbb5m6htf59wbjlsei.streamlit.app/

> The application is deployed using Streamlit Community Cloud.

---

## 📌 Project Overview

The Netflix AI Recommendation System is designed to help users discover movies and TV shows based on their interests.

Users can:

- 🎬 Select a movie or TV show
- 🤖 Get AI-powered recommendations
- ⭐ View movie ratings and information
- 🖼️ View movie posters using TMDB API
- 📊 Explore Netflix dataset analytics
- 🔥 View trending movies
- 📈 Explore popular genres
- 📚 View Netflix library statistics

The recommendation engine analyzes movie metadata such as:

- Title
- Director
- Cast
- Country
- Genre
- Description

These features are combined into a single text representation and converted into numerical vectors using **CountVectorizer**.

The system then calculates similarity using **Cosine Similarity**.

---

# ✨ Features

## 🎯 AI Movie Recommendation

Select a movie or TV show and receive the top 5 similar titles.

The recommendation engine uses:

**Content-Based Filtering + Cosine Similarity**

---

## 🔥 Trending Movies

The application retrieves trending movies using the **TMDB API** and displays their posters.

---

## 📊 Netflix Analytics Dashboard

The analytics section provides insights into the Netflix dataset, including:

- Total titles
- Number of Movies
- Number of TV Shows
- Release years
- Popular genres
- Content distribution
- Other dataset statistics

---

## 🎬 TMDB Integration

The application integrates with the **TMDB API** to retrieve:

- Movie posters
- Ratings
- Movie information
- Release information
- Trending movies

---

## 🎨 Modern Netflix-Inspired UI

The application includes:

- Netflix-inspired design
- Custom background
- Sidebar navigation
- Responsive layout
- Movie cards
- Interactive Streamlit components

---

## 🐳 Docker Support

The application is containerized using **Docker**.

The Docker image can be built and run independently from the local Python environment.

---

## ☸️ Kubernetes Deployment

The application was also deployed using **Kubernetes**.

The project includes:

- Kubernetes Deployment
- Kubernetes Service
- Containerized Streamlit application

This demonstrates the complete workflow:

```text
Python Application
        ↓
Docker
        ↓
Docker Hub
        ↓
Kubernetes
        ↓
Streamlit Application
