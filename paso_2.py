import glob
import json
import pandas as pd

all_data = []  # Lista para almacenar todos los datos de las playlists

files = glob.glob("raw_data/*.json")
print(len(files))

for file in files:
    playlist_data = []  # Lista para almacenar los datos de una playlist

    with open(file, 'r', encoding='utf-8') as f:
        datos = json.load(f)
        try:
            pais = file.split("-")[0].split("/")[1] # CUIDADO AMB AIXÔ la part .split("/") en mac o windows és diferent Posonun Try/except
        except:
            pais = file.split("-")[0].split("\\")[1]
        print(pais)

        for item in datos["items"]:
            artists = [artists["name"] for artists in item["track"]["album"]["artists"]]
            track_name = item["track"]["name"]
            popularity = item["track"]["popularity"]
            playlist = pais
            track_id = item["track"]["id"]

            # Obtener la duración de la pista en milisegundos
            duration_ms = item["track"]["duration_ms"]

            # Obtener si la pista es explícita o no
            explicit = item["track"]["explicit"]

            # Obtener el ID del primer artista
            primer_artista_id = item["track"]["artists"][0]["id"]

            # Obtener el ID de la playlist de la URL proporcionada
            playlist_url = datos["href"]
            playlist_id = playlist_url.split("/")[-2]

            tupla = (artists, track_name, popularity, primer_artista_id, playlist_id, playlist, track_id, duration_ms, explicit)
            playlist_data.append(tupla)

    df_playlist = pd.DataFrame(playlist_data,
                               columns=['artistas', 'track_name', 'popularity', 'primer_artista_id', 'playlist_id',
                                        'playlist', "track_id", "duration_ms", "explicit"])
    all_data.append(df_playlist)  # Agregar el DataFrame de esta playlist a la lista de todos los datos

# Concatenar todos los DataFrames en uno solo
df_combined = pd.concat(all_data, ignore_index=True)

# Guardar todos los datos en un solo archivo Excel
df_combined.to_excel("canciones_en_playlists.xlsx", index=False)
