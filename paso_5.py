import pandas as pd
import glob

lista = []
llista_2 = []
# Primero los Audio Features

dfs = glob.glob("paso2/*.xlsx")
for d in dfs:
    df = pd.read_excel(d)
    lista.append(df)

final = pd.concat(lista)
final.track_id = final.track_id.astype(str)

df2 = pd.read_excel("canciones_en_playlists.xlsx")
df2.track_id = df2.track_id.astype(str)

joined = pd.merge(final, df2, on="track_id", how="left")

print(joined.columns)

# Ahora los datos del artista

artists_dfs = glob.glob("paso3/*.xlsx")
for a in artists_dfs:
    artrist_df = pd.read_excel(a)
    llista_2.append(artrist_df)

final_2 = pd.concat(llista_2)
print(final_2)
print(final_2.columns)

final_2.artist_id = final_2.artist_id.astype(str)
joined.primer_artista_id = joined.primer_artista_id.astype(str)
joined["artist_id"] = joined["primer_artista_id"]

final_dataframe = pd.merge(final_2, joined, on="artist_id", how="left")

final_dataframe.to_excel("final_with_audio_and_artist_info.xlsx", index=False)
