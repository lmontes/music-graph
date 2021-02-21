import os
import codecs
from utils import extract_text_from_html


def parse_folder_files(folder, classname, file):
    for filename in sorted(os.listdir(folder)):
        print(filename)
        with codecs.open(u"%s/%s" % (folder, filename), encoding="utf-8") as f:
            text = extract_text_from_html(f.read())
            id = filename.replace(".html", "")
            file.write(f"{id};{classname};{text}\n")


with open("data/dataset.csv", "w") as dataset_file:
    dataset_file.write("id;class;text\n")
    parse_folder_files("raw-data/musician", "musician", dataset_file)
    parse_folder_files("raw-data/other", "other", dataset_file)
