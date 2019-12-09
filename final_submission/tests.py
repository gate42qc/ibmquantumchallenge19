from utils import run_and_print_results
from graph import Graph, Konbini
from main import run_coloring_grover


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


def run_test_for_graph(graph: Graph):
    qc = run_coloring_grover(graph, 2)
    results = run_and_print_results(qc)
    most_probable = list(results.keys())
    valid_total_solutions = 0
    number_of_valid_states_found = 0
    found_invalid = False

    for color_bitstring in most_probable:
        color_bitstring_corrected = color_bitstring[::-1]
        colored = graph.get_colored(color_bitstring_corrected)
        if not colored.is_coloring_valid():
            found_invalid = True
            # print(f"Not valid coloring: {color_bitstring_corrected} with count of {results[color_bitstring]}")
        else:
            valid_total_solutions += 1

        if not found_invalid:
            number_of_valid_states_found += 1

    print(f"Total valid solutions: {valid_total_solutions}")
    print(f"From which algorithm found: {number_of_valid_states_found}")


if __name__ == '__main__':
    run_test_for_graph(get_4_vertex_graph())
    run_test_for_graph(get_5_vertex_graph())
