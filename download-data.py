import csv
import time
import requests

from utils import id_from_url


with open("data/classes.csv", "r") as f_cl:
    reader = csv.DictReader(f_cl, delimiter=";")
    for row in reader:
        article = row["url"]
        classification = row["class"]

        print(f"Downloading article: {article}")
        try:
            url = f"https://en.wikipedia.org/wiki/{article}"
            response = requests.get(url)
            if response.status_code == 200:
                article_filename = id_from_url(article)
                with open(f"raw-data/{classification}/{article_filename}.html", "wb") as f:
                    f.write(response.content)
                print(f"Downloaded article: {article} {article_filename}")
            else:
                print(f"Error downloading article from {url}")
            time.sleep(0.5)
        except Exception as e:
            print(f"Exception downloading article from {url}")
            time.sleep(1)
