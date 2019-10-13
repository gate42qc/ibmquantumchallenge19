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
    graph = Graph(5, [
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

    # graph.redefine_groups([
    #     [(0, 1), (0, 2), (0, 4)],
    #     [(1, 2), (1, 3), (1, 'A')],
    #     [(2, 'A')],
    #     [(3, 4)],
    # ])

    return graph


def get_ibm_graph() -> Graph:
    graph = Graph(7, [
        (0, 1), (0, 2), (0, 3), (1, 3),
        (1, 4), (2, 3), (2, 5), (2, 6),
        (3, 4), (3, 5), (3, 6),
        (4, 6), (5, 6),
    ], [
        (Konbini.get_by_name('A'), 0),
        (Konbini.get_by_name('B'), 1),
        (Konbini.get_by_name('A'), 2),
        (Konbini.get_by_name('C'), 2),
        (Konbini.get_by_name('A'), 3),
        (Konbini.get_by_name('B'), 4),
        (Konbini.get_by_name('D'), 5),
        (Konbini.get_by_name('D'), 6)
    ])
    # print(graph.groups)

    # graph.redefine_groups([
    #     [(0, 1), (0, 'A'), (6, 4), (6, 5)],
    #     [(2, 0), (2, 5), (2, 6), (2, 'A'), (1, 4)],
    #     [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 'A')],
    # ])

    graph.redefine_groups([
        [(0, 1), (6, 4), (6, 5)],  # 1, 4, 5
        [(2, 0), (2, 5), (2, 6), (2, 'C'), (1, 4)],  # 0, 5, 6, 2, 4
        [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6)],  # 0, 1, 2, 4, 5, 6
    ])

    return graph
