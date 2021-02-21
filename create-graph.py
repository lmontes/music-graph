import re
import os
import csv
import codecs
from bs4 import BeautifulSoup

from utils import clean_title, id_from_url


file_path = "raw-data/musician/"
node_names = {}
node_files = {}
node_in_degree = {}
edge_weights = {}
file_names = set()
file_to_title = {}
file_links = {}


with open("data/classes.csv") as f:
    reader = csv.DictReader(f, delimiter=";")
    url_mapping = {row["md5"]: row["url"] for row in reader}


# Open all files and get all links to other wikipedia pages
for article in sorted(os.listdir(file_path)):
    with codecs.open(u"%s/%s" % (file_path, article), encoding="utf-8") as file:
        soup = BeautifulSoup(file.read(), "html.parser")
    
    file_name = article.replace(".html", "")
    file_names.add(file_name)
    page_title = clean_title(soup.find(id="firstHeading").get_text())
    print(article, page_title)
    file_to_title[file_name] = page_title
    file_links[file_name] = []
    
    for link in soup.find("div", {"id": "bodyContent"}).findAll("a", href=re.compile("^(/wiki/)((?!:).)*$")):
        if 'href' in link.attrs:
            destination = link["href"].replace("/wiki/", "").split("#")[0]
            destination = id_from_url(destination)
            if destination != file_name:
                file_links[file_name].append(destination)


# Filter all links to get only links between the pages we have
for file in file_links:
    source = file
    node_names[source] = file_to_title[file]
    node_files[source] = file

    for destination in file_links[file]:
        if destination in file_names:
            if source != destination:
                print(source, destination)

                edge = (source, destination)

                if edge not in edge_weights:
                    edge_weights[edge] = 0
                edge_weights[edge] += 1

                if destination not in node_in_degree:
                    node_in_degree[destination] = 0
                node_in_degree[destination] += 1


# Generate numeric identifiers in order to be more efficient
short_identifiers = {key:id for id, key in enumerate(file_links.keys(), start=1)}


# Generate CSV files with the resulting graph structure
with open("data/graph-nodes.csv", "w") as nodes_csv:
    nodes_csv.write("id;name;url;size\n")
    for node_id in node_names:
        size = 1
        if node_id in node_in_degree:
            size = node_in_degree[node_id] * 10
        nodes_csv.write(f"{short_identifiers[node_id]};\"{node_names[node_id]}\";\"{url_mapping[node_id]}\";{size}\n")


with open("data/graph-edges.csv", "w") as edges_csv:
    edges_csv.write("src;dst;weight\n")
    for e in edge_weights:
        edges_csv.write(f"{short_identifiers[e[0]]};{short_identifiers[e[1]]};{edge_weights[e]}\n")
