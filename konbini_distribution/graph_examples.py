from graph import Graph, Konbini


def get_4_vertex_graph():
    return Graph(4, [
        (0, 1),
        (1, 2),
        (2, 3),
        (3, 0),
        (0, 2),
    ], [
        (Konbini.get_by_name('A'), 0),
        (Konbini.get_by_name('D'), 1),
    ])


def get_5_vertex_graph():
    return Graph(5, [
        (0, 1),
        (0, 2),
        (0, 4),
        (1, 2),
        (1, 3),
        (3, 4),
    ], [
        (Konbini.get_by_name('A'), 1),
        (Konbini.get_by_name('A'), 2),
        (Konbini.get_by_name('B'), 2),
        (Konbini.get_by_name('B'), 3),
        (Konbini.get_by_name('C'), 0),
    ])
