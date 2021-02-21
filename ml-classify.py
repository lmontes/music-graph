import os
import codecs

from model import Classifier
from utils import extract_text_from_html


model = Classifier("data/model.pkl")


for filename in sorted(os.listdir("raw-data/unclassified")):
    with codecs.open(f"raw-data/unclassified/{filename}", encoding="utf-8") as f:
        text = extract_text_from_html(f.read())

        classification = model.predict(text)
    
        print(filename, classification)
        if classification != "unclassified":
            os.rename(f"raw-data/unclassified/{filename}", f"raw-data/{classification}/{filename}")
