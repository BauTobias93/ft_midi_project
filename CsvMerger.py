import datetime
import os
import glob
from time import strftime

import pandas as pd
import re
import random


def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)


PATH = "C:\\Users\\preis\\Documents\\FT\\ft_midi_project\\csv_files"
EXT = "*.csv"
all_csv_files = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in glob.glob(os.path.join(path, EXT))]
random.shuffle(all_csv_files)
csv_files = []

current_case_id = 0
pattern = re.compile(r"(.*)\\(.*)\\(.*).csv")
songs_pre_genre = {}

#handle prioritised files
priority = ["C:\\Users\\preis\\Documents\\FT\\ft_midi_project\\csv_files\\classic\\haydn_33_1.csv"]
for file in priority:
    all_csv_files.insert(0, file)

for f in all_csv_files:
    print(f)
    df = pd.read_csv(f)
    genre = pattern.match(f).group(2)
    song_name = pattern.match(f).group(3)
    if genre in songs_pre_genre:
        if songs_pre_genre[genre] >= 20:
            continue
        else:
            songs_pre_genre[genre] = songs_pre_genre[genre] + 1
    else:
        songs_pre_genre[genre] = 1

    case_id_col = []
    octave_col = []
    note_col = []
    real_time_col = []
    genre_col = []
    song_name_col = []
    for index, row in df.iterrows():
        case_id_col.append(current_case_id)
        octave_col.append(row["note_name"][-1])
        note_col.append(row["note_name"][:-1].replace("-", ""))
        real_time_col.append(pd.to_datetime(truncate((row["start_time"] / (row["tempo"] / 60)), 2), unit="s"))
        genre_col.append(genre)
        song_name_col.append(song_name)

    df.insert(0, 'case_id', case_id_col)
    df.insert(2, 'octave', octave_col)
    df.insert(2, 'actual_note', note_col)
    df.insert(6, 'real_time', real_time_col)
    df.insert(2, 'genre', genre_col)
    df.insert(3, 'song_name', song_name)
    csv_files.append(df)

    current_case_id += 1

combined_csv = pd.concat(csv_files)
combined_csv.rename({'Unnamed: 0': 'note'}, axis=1, inplace=True)
combined_csv.to_csv("csv_files_merged/combined_csv.csv", index=False, encoding='utf-8-sig')
