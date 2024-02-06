import pandas as pd
import streamlit as st
import pickle
import requests


def fetch_poster(movie_id):
    url = "https://api.themoviedb.org/3/movie/{}?api_key=5e2fabdcae25958b56f076b67fad2e11&language=en-US".format(movie_id)
    data = requests.get(url)
    data = data.json()
    poster_path = data['poster_path']
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    return full_path

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]

    distances = similarity[movie_index]

    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended = []

    recommended_movie_posters = []

    for i in movies_list:
        movie_id = movies.iloc[i[0]].movie_id
        recommended.append(movies.iloc[i[0]].title)
        recommended_movie_posters.append(fetch_poster(movie_id))
    return recommended, recommended_movie_posters


selected_movie_name = st.title('Movie Recommender System')
movies_list = pickle.load(open('movies.pkl', 'rb'))
movies = pd.DataFrame(movies_list)

similarity = pickle.load(open('similarity.pkl', 'rb'))

selected_movie = st.selectbox(
    "Type or select a movie from the dropdown",
    movies_list['title'].values
)

if st.button('Show Recommendation'):
    recommended, recommended_movie_posters = recommend(selected_movie)
    col1, col2, col3, col4, col5 = st.columns(5)
    with col1:
        st.text(recommended[0])
        st.image(recommended_movie_posters[0])
    with col2:
        st.text(recommended[1])
        st.image(recommended_movie_posters[1])
    with col3:
        st.text(recommended[2])
        st.image(recommended_movie_posters[2])
    with col4:
        st.text(recommended[3])
        st.image(recommended_movie_posters[3])
    with col5:
        st.text(recommended[4])
        st.image(recommended_movie_posters[4])