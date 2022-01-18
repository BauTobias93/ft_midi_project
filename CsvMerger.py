import os
import glob
import pandas as pd


def truncate(num, n):
    integer = int(num * (10**n))/(10**n)
    return float(integer)


PATH = "C:/Users/preis/Documents/FT/ft_midi_project/csv_files"
EXT = "*.csv"
all_csv_files = [file
                 for path, subdir, files in os.walk(PATH)
                 for file in glob.glob(os.path.join(path, EXT))]

csv_files = []

current_case_id = 0

for f in all_csv_files:
    print(f)
    df = pd.read_csv(f)

    case_id_col = []
    octave_col = []
    note_col = []
    real_time_col = []
    for index, row in df.iterrows():
        case_id_col.append(current_case_id)
        octave_col.append(row["note_name"][-1])
        note_col.append(row["note_name"][:-1].replace("-", ""))
        real_time_col.append(truncate((row["start_time"] / (row["tempo"] / 60)), 2))

    df.insert(0, 'case_id', case_id_col)
    df.insert(2, 'octave', octave_col)
    df.insert(2, 'note', note_col)
    df.insert(6, 'real_time', real_time_col)
    csv_files.append(df)

    current_case_id += 1

combined_csv = pd.concat(csv_files)
combined_csv.rename({'Unnamed: 0': 'note'}, axis=1, inplace=True)
combined_csv.to_csv("csv_files_merged/combined_csv.csv", index=False, encoding='utf-8-sig')
