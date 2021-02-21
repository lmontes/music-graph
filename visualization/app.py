import csv
import json
from flask import Flask, request, send_from_directory


app = Flask(__name__, static_url_path='')


def get_graph():
    with open("../data/graph-communities.csv") as gc:
        gc_reader = csv.DictReader(gc, delimiter=";")
        communities = {int(r["id"]): int(r["community"]) for r in gc_reader}
        print(communities)

    nodes = []
    with open("../data/graph-nodes.csv") as gn:
        gn_reader = csv.DictReader(gn, delimiter=";")

        for r in gn_reader:
            id = int(r["id"])
            nodes.append({
                "id": id,
                "label": r["name"],
                "group": int(communities[id]) if id in communities else -1,
                "value": int(r["size"]),
                "url": r["url"]
            })

    edges = []
    with open("../data/graph-edges.csv") as ge:
        ge_reader = csv.DictReader(ge, delimiter=";")

        for r in ge_reader:
            edges.append({
                "from": int(r["src"]),
                "to": int(r["dst"]),
                "weight": int(r["weight"])
            })
    return nodes, edges


@app.route("/")
def root():
    return send_from_directory("", "index.html")


@app.route("/static/<path:path>")
def send_js(path):
    return send_from_directory("static", path)


@app.route("/positions", methods=["POST"])
def positions():
    pos = json.loads(request.data)
    pos = {int(key): pos[key] for key in pos}

    nodes, edges = get_graph()
    for n in nodes:
        id = n["id"]
        if id in pos:
            n["x"] = pos[id]["x"]
            n["y"] = pos[id]["y"]

    nodes_js = []
    for n in nodes:
        id = n["id"]
        label = n["label"]
        group = n["group"]
        value = n["value"]
        url = n["url"]
        x = n["x"]
        y = n["y"]
        nodes_js.append(f"{{id:{id},label:\"{label}\",group:{group},value:{value},url:\"{url}\",x:{x},y:{y}}}")
    nodes_str = "var nodes = [\n" + ",\n".join(nodes_js) + "\n];"

    edges_js = []
    for e in edges:
        src = e["from"]
        dst = e["to"]
        weight = e["weight"]
        if weight > 1:
            edges_js.append(f"{{from:{src},to:{dst},weight:{weight}}}")
    edges_str = "var edges = [\n" + ",\n".join(edges_js) + "\n];"

    with open("static/gdata.js", "w") as f:
        f.write(nodes_str)
        f.write("\n")
        f.write(edges_str)
    return ""


@app.route("/graph", methods=["GET"])
def graph():
    nodes, edges = get_graph()
    return {"nodes": nodes, "edges": edges}


if __name__ == "__main__":
    app.run( host="0.0.0.0", port=8080)