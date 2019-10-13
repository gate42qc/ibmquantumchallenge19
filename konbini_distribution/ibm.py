from coloring_main import run_coloring_grover
from graph import Graph, Konbini
from qiskit import QuantumCircuit, QuantumRegister
from utils import get_cost
from math import pi

from graph_examples import get_ibm_graph


def get_hackathon_circuit():
    graph = get_ibm_graph()
    qc = run_coloring_grover(graph, 5)
    return qc


def get_ibm_cost():
    graph = get_ibm_graph()
    qc = run_coloring_grover(graph, 5)

    cost = get_cost(qc)

    print(f"Number of ancilla needed: {graph.get_ancilla_size_needed()}")
    print(f"Cost was: {cost}")


if __name__ == '__main__':
    # reg = QuantumRegister(2)
    # qc = QuantumCircuit(reg)
    # qc.crz(pi, 0, 1)
    # cost = get_cost(qc)
    # print(f"Cost was: {cost}")
    get_ibm_cost()

