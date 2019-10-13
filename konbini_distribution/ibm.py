from coloring_main import run_coloring_grover
from graph import Graph, Konbini
from utils import get_cost


def get_ibm_graph() -> Graph:
    return Graph(7, [
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


def get_hackathon_circuit():
    graph = get_ibm_graph()
    qc = run_coloring_grover(graph, 5)
    return qc


def get_ibm_cost():
    graph = get_ibm_graph()
    qc = run_coloring_grover(graph, 5)

    cost = get_cost(qc)

    print(f"Cost was: {cost}")


if __name__ == '__main__':
    get_ibm_cost()

