from main import run_coloring_grover
from utils import get_cost
from hackathon_graph import get_hackathon_graph


def get_hackathon_circuit():
    graph = get_hackathon_graph()
    qc = run_coloring_grover(graph, 5)
    return qc


def get_cost_for_hackathon_graph():
    graph = get_hackathon_graph()
    qc = run_coloring_grover(graph, 5)

    cost = get_cost(qc)

    total_qubits = graph.get_ancilla_size_needed() + len(graph.vertices) * graph.color_bit_length

    print(f"Number of qubits needed: {total_qubits}")
    print(f"Cost was: {cost}")


if __name__ == '__main__':
    get_cost_for_hackathon_graph()

