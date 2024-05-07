import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from pathlib import Path
import time
import random
import os


# Inicializar cliente de autenticación de Spotify
client_credentials_manager = SpotifyClientCredentials(client_id='xxxxxxxxxxxxxxxxxxxxxxxxx',client_secret='xxxxxxxxxxxxxxxxxxxxxxx')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Por cada cancion en el dataset vamos a extraer datos
llista_de_rows = []

def get_artist_info(artist):
    artist_id = artist

    try:
        artist_info = spotify.artist(artist_id)

        # Guardem la ROW amb les dades noves en una llista
        data = {}
        data["artist_followers"] = artist_info["followers"]["total"]
        data["artist_genres"] = artist_info["genres"]
        data["artist_id"] = artist_id
        data["artist_popularity"] = artist_info["popularity"]
        final = pd.DataFrame.from_dict([data], orient='columns')
        final.to_excel(f"paso3/{artist}-artist_info.xlsx", index=False)

    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 429:
            print(e)
            print("Error 429 Too many requests Retry in 60 seconds")
            time.sleep(1800)
            get_artist_info(artist)
        if e.http_status == 503:
            print(e)
            print("Error 503 Retry in 60 seconds")
            time.sleep(1800)
            get_artist_info(artist)
        else:
            raise e

df = pd.read_excel("canciones_en_playlists.xlsx")

artist_ids = df["primer_artista_id"].unique()
artist_ids  = artist_ids.tolist()
jobs = len(artist_ids)

for artist in artist_ids :
    job = artist_ids.index(artist)
    artist_id = artist
    wait_time = random.randint(2,3)
    print(f"working on job {job} of {jobs} | Wait time {wait_time}")
    path = f"paso3/{artist}-artist_info.xlsx"
    if not os.path.exists(path):
        get_artist_info(artist)
        time.sleep(wait_time)
    else:
        print(f"{artist} ja descarregat")
        pass


