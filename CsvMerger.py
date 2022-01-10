import os
import glob
import pandas as pd

os.chdir('csv_files')
all_filenames = [i for i in glob.glob('*.{}'.format('csv'))]

csv_files = []

current_case_id = 0

for f in all_filenames:
    df = pd.read_csv(f)

    case_id_col = []
    octave_col = []
    note_col = []
    for index, row in df.iterrows():
        case_id_col.append(current_case_id)
        octave_col.append(row["note_name"][-1])
        note_col.append(row["note_name"][:-1].replace("-", ""))

    df.insert(0, 'case_id', case_id_col)
    df.insert(2, 'octave', octave_col)
    df.insert(2, 'note', note_col)
    csv_files.append(df)

    current_case_id += 1

combined_csv = pd.concat(csv_files)
combined_csv.rename({'Unnamed: 0': 'note'}, axis=1, inplace=True)
os.chdir('../csv_files_merged')
combined_csv.to_csv("combined_csv.csv", index=False, encoding='utf-8-sig')
