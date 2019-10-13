import networkx as nx

from graph import Graph


def draw(graph: Graph):
    nx_graph = nx.Graph()
    nx_graph.add_nodes_from([v.number for v in graph.vertices])
    nx_graph.add_edges_from([(start.number, end.number) for start, end in graph.edges])
