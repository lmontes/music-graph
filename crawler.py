import os
import re
import csv
import time
import requests

from bs4 import BeautifulSoup
from collections import deque

from model import Classifier
from utils import extract_text_from_html, id_from_url


model = Classifier("data/model.pkl")


visited = set()
with open("data/classes.csv", "r") as visited_file:
    reader = csv.DictReader(visited_file, delimiter=";")
    visited = set([row["url"] for row in reader])


visited_file = open("data/classes.csv", "a")

# Set one seed to start the crawler
to_visit = [
    "Metallica"
]
to_visit_queue = deque(to_visit)
to_visit_set = set(to_visit)


print("Already collected : %s" % len(visited))


while len(to_visit_queue) > 0:
    article = to_visit_queue.popleft()
    to_visit_set.remove(article)

    print("Article: %s" % article)
    article_filename = id_from_url(article)

    visited.add(article)
    visited_file.write(f"{article};{article_filename};\n")
    visited_file.flush()

    try:
        url = "https://en.wikipedia.org/wiki/%s" % article

        response = requests.get(url)
        if response.status_code == 200:
            with open(f"raw-data/unclassified/{article_filename}.html", "wb") as f:
                f.write(response.content)
        else:
            print(f"Error downloading article from {url}")

        soup = BeautifulSoup(response.content, "html.parser")
        for tag_remove in soup(["script", "style"]):
            tag_remove.decompose()
        text = extract_text_from_html(file_content)

        classification = model.predict(text)

        page_title = soup.find(id="firstHeading").get_text()

        print("Title: %s , %s" % (page_title, classification))
        
        if classification != "unclassified":
            os.rename(f"raw-data/unclassified/{article_filename}.html", f"raw-data/{classification}/{article_filename}.html")
        
        # Continue search if classification is musician or unclassified (no model)
        if classification == "musician" or classification is "unclassified":
            for link in soup.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
                if 'href' in link.attrs:
                    new_article = link["href"].replace("/wiki/", "")
                    if new_article not in visited and new_article not in to_visit_set and "disambiguation" not in new_article:
                        to_visit_queue.append(new_article)
                        to_visit_set.add(new_article)
        time.sleep(1)
    except Exception as e:
        print(url, e)
