import json
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from pathlib import Path

# Inicializar cliente de autenticación de Spotify
client_credentials_manager = SpotifyClientCredentials(client_id='XXXXXXXXXXXXXXXXXXXXXXXXXXXXX',client_secret='XXXXXXXXXXXXXXXXXXXXXXXXX')
spotify = spotipy.Spotify(client_credentials_manager=client_credentials_manager)

# CARGAMOS LAS "ID" de las playlists que queremos extraer.
# TODAS LAS ID ESTAN EN UN EXCEL.
playlists = pd.read_excel("playlist.xlsx")
print(playlists)

# Iterar sobre los países y obtener los artistas más escuchados
for index, row in playlists.iterrows():
    pais = row["COUNTRY"]
    playlist_id = row["ID"]
    playlist_name = row["NAME"]
    file_path = Path(f'raw_data/{pais}-{playlist_id}.json')

    if file_path.exists():
        print(f"La playlist {playlist_id} ya se ha descargado")
        pass
    else:
        api_response = spotify.playlist_items(playlist_id)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(api_response, f, ensure_ascii=False, indent=4)
