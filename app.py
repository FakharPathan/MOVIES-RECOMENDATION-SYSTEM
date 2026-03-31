import streamlit as st
import pickle
import pandas as pd
import requests

# Function to fetch posters from API
def get_movie_poster(movie_id):
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
    data = requests.get(url).json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']

# Load Data
movie_df = pickle.load(open('movies.pkl', 'rb'))
dist_matrix = pickle.load(open('similarity.pkl', 'rb'))

st.title('Movie Recommender System')

selected_movie = st.selectbox('Select a movie:', movie_df['title'].values)

if st.button('Recommend'):
    movie_idx = movie_df[movie_df['title'] == selected_movie].index[0]
    scores = dist_matrix[movie_idx]
    
    # Sorting and Slicing (Top 5)
    top_five = sorted(list(enumerate(scores)), reverse=True, key=lambda x: x[1])[1:6]
    
    cols = st.columns(5)
    for i, (idx, score) in enumerate(top_five):
        with cols[i]:
            st.text(movie_df.iloc[idx].title)
            st.image(get_movie_poster(movie_df.iloc[idx].movie_id))
