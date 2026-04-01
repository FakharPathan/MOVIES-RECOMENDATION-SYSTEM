import streamlit as st
import pickle
import numpy as np
import pandas as pd
import requests
import os

BASE_DIR = os.path.dirname(os.path.realpath(__file__))

@st.cache_resource
def load_data():
    sim_path = "/tmp/similarity.npy"  
    
    if not os.path.exists(sim_path) or os.path.getsize(sim_path) < 1000000:
        file_id = "TERA_NAYA_FILE_ID" 
        session = requests.Session()
        url = f"https://drive.google.com/uc?export=download&id={file_id}"
        resp = session.get(url, stream=True)
        token = None
        for key, value in resp.cookies.items():
            if key.startswith("download_warning"):
                token = value
        if token:
            url = f"https://drive.google.com/uc?export=download&id={file_id}&confirm={token}"
            resp = session.get(url, stream=True)
        with open(sim_path, "wb") as f:
            for chunk in resp.iter_content(32768):
                if chunk:
                    f.write(chunk)

    movie_df = pickle.load(open(os.path.join(BASE_DIR, "movies.pkl"), "rb"))
    
    dist_matrix = np.load(sim_path)
    
    return movie_df, dist_matrix
