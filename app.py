import streamlit as st
import pickle
import pandas as pd
import requests
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

@st.cache_resource
def load_data():
    sim_path = "/tmp/similarity.pkl"
    if not os.path.exists(sim_path) or os.path.getsize(sim_path) < 1000000:
        file_id = "10MqN_cT1Z1H9SNDBOAVqzr2zHrRxWt3b"
        session = requests.Session()
        url     = f"https://drive.google.com/uc?export=download&id={file_id}"
        resp    = session.get(url, stream=True)
        # Large file confirm token handle karo
        token   = None
        for key, value in resp.cookies.items():
            if key.startswith("download_warning"):
                token = value
        if token:
            url  = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={token}"
            resp = session.get(url, stream=True)
        with open(sim_path, "wb") as f:
            for chunk in resp.iter_content(32768):
                if chunk:
                    f.write(chunk)

    movie_df    = pickle.load(open(os.path.join(BASE_DIR, "movies.pkl,"), "rb"))
    dist_matrix = pickle.load(open(sim_path, "rb"))
    return movie_df, dist_matrix

movie_df, dist_matrix = load_data()

def get_movie_poster(movie_id):
    try:
        url    = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US'
        data   = requests.get(url, timeout=5).json()
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
streamlit
pandas
scikit-learn
requests
