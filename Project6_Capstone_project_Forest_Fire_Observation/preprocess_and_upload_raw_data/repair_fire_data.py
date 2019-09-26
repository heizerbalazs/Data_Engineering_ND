import json
import re
import os
import logging

patterns = ['"acq_date": ', '"acq_time": ', '"satellite": ', '"daynight": ', '"instrument": ']

def replace_with_string(text,pattern):
    index = text.find(pattern)
    if index != None:
        return "\t\t"+pattern+'"'+text[index+len(pattern):-2]+'",\n'

def get_file_paths(directory):
    files = os.listdir(directory)
    for i, file in enumerate(files):
        files[i] = directory+file
    return files[:-1]

def repair_json(file_path):
    with open(file_path, 'r') as f:
        rows = f.readlines()

    for i, row in enumerate(rows):
        for pattern in patterns:
            index = row.find(pattern)
            if index != -1:
                rows[i] = replace_with_string(row,pattern)

    with open(file_path,"w") as f:
        f.writelines(rows)

if __name__ == "__main__":
    file_paths = get_file_paths('../data/Forestfires/')

    for file_path in file_paths:
        logging.warning("{} is open.".format(file_path))
        repair_json(file_path)
        logging.warning("{} is repaired.".format(file_path))
