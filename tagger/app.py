import os
import csv
from flask import Flask, request, abort, send_from_directory


data_dir = "../data"
raw_data_dir = "../raw-data"

index = -1
url_mapping = {}
unclassified_pages = []

app = Flask(__name__)


@app.route("/")
def root():
    global index, unclassified_pages

    index = -1
    unclassified_pages = list(sorted(os.listdir(os.path.join(raw_data_dir, "unclassified"))))

    return send_from_directory("", "index.html")


@app.route("/next", methods=["GET"])
def next():
    global index

    index +=1
    if index < len(unclassified_pages):
        key = unclassified_pages[index].replace(".html", "")
        return {
            "id": key,
            "url": url_mapping[key]
        }
    abort(404)


@app.route("/tag", methods=["POST"])
def tag():
    print(request.json)
    page = request.json["id"]
    cls_ = request.json["class"]

    page = f"{page}.html"
    src_path = os.path.join(raw_data_dir, "unclassified", page)

    if cls_ == "musician":
        dst_path = os.path.join(raw_data_dir, "musician",  page)
    else:
        dst_path = os.path.join(raw_data_dir, "other",  page)
    
    os.rename(src_path, dst_path)
    return {}


if __name__ == "__main__":
    with open(os.path.join(data_dir, "classes.csv")) as f:
        reader = csv.DictReader(f, delimiter=";")
        url_mapping = {row["md5"]: row["url"] for row in reader}
    
    app.run(host="0.0.0.0", port=8000)