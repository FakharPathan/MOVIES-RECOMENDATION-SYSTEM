import streamlit as st
import pickle
import pandas as pd
import requests
import os
import gdown

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

@st.cache_resource
def load_data():
    if not os.path.exists("similarity.pkl"):
        gdown.download("https://drive.google.com/uc?id=10MqN_cT1Z1H9SNDBOAVqzr2zHrRxWt3b", "similarity.pkl", quiet=False)
    movie_df     = pickle.load(open(os.path.join(BASE_DIR, "movies.pkl"), "rb"))
    dist_matrix  = pickle.load(open("similarity.pkl", "rb"))
    return movie_df, dist_matrix

movie_df, dist_matrix = load_data()

def get_movie_poster(movie_id):
    try:
        url  = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        data = requests.get(url, timeout=5).json()
        poster = data.get('poster_path')
        return "https://image.tmdb.org/t/p/w500/" + poster if poster else "https://via.placeholder.com/500x750?text=No+Image"
    except:
        return "https://via.placeholder.com/500x750?text=No+Image"

st.title('🎬 Movie Recommender System')

selected_movie = st.selectbox('Select a movie:', movie_df['title'].values)

if st.button('Recommend'):
    with st.spinner('Finding recommendations...'):
        movie_idx = movie_df[movie_df['title'] == selected_movie].index[0]
        scores    = dist_matrix[movie_idx]
        top_five  = sorted(list(enumerate(scores)), reverse=True, key=lambda x: x[1])[1:6]

    cols = st.columns(5)
    for i, (idx, score) in enumerate(top_five):
        with cols[i]:
            st.image(get_movie_poster(movie_df.iloc[idx].movie_id))
            st.caption(movie_df.iloc[idx].title)
