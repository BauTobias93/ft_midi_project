import os
from MidiConverter import convert

def run():
    input_path = "data"
    output_path = "csv_files"

    for dir in os.listdir(input_path):
        in_path = os.path.join(input_path, dir)
        if os.path.isdir(in_path):
            out_path = os.path.join(output_path, dir)
            convert(in_path, out_path)

if __name__ == "__main__":
    run()