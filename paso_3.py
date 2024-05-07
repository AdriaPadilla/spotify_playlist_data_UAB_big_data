import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from pathlib import Path
import time
import random
import os


# Inicializar cliente de autenticación de Spotify
client_credentials_manager = SpotifyClientCredentials(client_id='XXXXXXXXXXXXXXXX',client_secret='XXXXXXXXXXXXXXXXXXX')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# Por cada cancion en el dataset vamos a extraer datos
llista_de_rows = []

def get_audio_features(track):
    track_id = track # pillamos el track_id
    # hacemos la petición a la API de Spotify
    # DOCUMENTACION: https://spotipy.readthedocs.io/en/2.22.1/#spotipy.client.Spotify.audio_features
    try:
        audio_features = spotify.audio_features(track_id)

        # Guardem la ROW amb les dades noves en una llista
        data = pd.DataFrame.from_dict(audio_features, orient='columns')
        data["track_id"] = track_id
        data.to_excel(f"paso2/{track_id}-audio_features.xlsx", index=False)
         # dormim mig segon per no saturar la API de Spotigy

    except spotipy.exceptions.SpotifyException as e:
        if e.http_status == 429:
            print(e)
            print("Error 429 Too many requests Retry in 60 seconds")
            time.sleep(1800)
            get_audio_features(row)
        if e.http_status == 503:
            print(e)
            print("Error 503 Retry in 60 seconds")
            time.sleep(1800)
            get_audio_features(row)
        else:
            raise e

df = pd.read_excel("canciones_en_playlists.xlsx")

tracks = df["track_id"].unique()
tracks = tracks.tolist()
jobs = len(tracks)

for track in tracks:
    job = tracks.index(track)
    track_id = track
    wait_time = random.randint(2,3)
    print(f"working on job {job} of {jobs} | Wait time {wait_time}")
    path = f"paso2/{track_id}-audio_features.xlsx"
    if not os.path.exists(path):
        get_audio_features(track)
        time.sleep(wait_time)
    else:
        print(f"{track} ja descarregat")
        pass


