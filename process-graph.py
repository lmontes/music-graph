import pandas as pd
import networkx as nx
import community as cl


dfn = pd.read_csv("data/graph-nodes.csv", delimiter=";")
dfe = pd.read_csv("data/graph-edges.csv", delimiter=";")

nodes = dfn["id"].tolist()
edges = list(dfe.itertuples(index=False, name=None))


G = nx.Graph()
G.add_nodes_from(nodes)
G.add_weighted_edges_from(edges)

partitions = cl.community_louvain.best_partition(G)

with open("data/graph-communities.csv", "w") as f:
    f.write("id;community\n")
    for p in partitions:
        f.write(f"{p};{partitions[p]}\n")
