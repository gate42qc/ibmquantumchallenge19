from graph import Graph, Konbini
from qiskit import QuantumCircuit, QuantumRegister


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
    KONBINI_A = Konbini.get_by_name('A')
    KONBINI_B = Konbini.get_by_name('B')
    KONBINI_C = Konbini.get_by_name('C')
    KONBINI_D = Konbini.get_by_name('D')
    tmp = KONBINI_A.encoding
    KONBINI_A.encoding = KONBINI_C.encoding
    KONBINI_C.encoding = tmp

    graph = Graph(7, [
        (0, 1), (0, 2), (0, 3), (1, 3),
        (1, 4), (2, 3), (2, 5), (2, 6),
        (3, 4), (3, 5), (3, 6),
        (4, 6), (5, 6),
    ], [
        (KONBINI_A, 0),
        (KONBINI_B, 1),
        (KONBINI_A, 2),
        (KONBINI_C, 2),
        (KONBINI_A, 3),
        (KONBINI_B, 4),
        (KONBINI_D, 5),
        (KONBINI_D, 6)
    ])

    def get_finalizer_circuit(graph: Graph):
        register = QuantumRegister(len(graph.vertices) * graph.color_bit_length)
        qc = QuantumCircuit(register)

        for vertex in graph.vertices:
            qc.x(vertex.get_qubits(register)[1])
            qc.cx(vertex.get_qubits(register)[1], vertex.get_qubits(register)[0])
            qc.x(vertex.get_qubits(register)[1])

        return qc

    graph.set_state_finalizer(get_finalizer_circuit)

    # by redefining groups you can reduce the cost, here we experiment with different groupings

    # graph.redefine_groups([
    #     [(0, 1), (0, 'A'), (6, 4), (6, 5)],
    #     [(2, 0), (2, 5), (2, 6), (2, 'A'), (1, 4)],
    #     [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (3, 'A')],
    # ])  # cost 37 455

    graph.redefine_groups([
        [(0, 1), (6, 4), (6, 5)],  # 1, 4, 5
        [(2, 0), (2, 5), (2, 6), (2, 'C'), (1, 4)],  # 0, 5, 6, 2, 4
        [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6)],  # 0, 1, 2, 4, 5, 6
    ])  # cost 34185 + 4qubits

    # graph.redefine_groups([
    #     [(2, 0), (2, 5), (2, 6), (2, 'C'), (1, 4), (6, 4), (6, 5)],
    #     [(3, 0), (3, 1), (3, 2), (3, 4), (3, 5), (3, 6), (0, 1)],
    # ])  # cost 42855 + 3qubits

    # graph.redefine_groups([
    #     [(0, 1), (6, 4), (6, 5)],  # 1, 4, 5
    #     [(2, 0), (2, 5), (2, 6), (2, 'C')],  # 0, 5, 6, 2, 4
    #     [(3, 5), (3, 6), (1, 4)],
    #     [(3, 0), (3, 1), (3, 2), (3, 4)],  # 0, 1, 2, 4, 5, 6
    # ])  # cost 35635

    # graph.redefine_groups([
    #     [(0, 1), (6, 4), (6, 5)],  # 1, 4, 5
    #     [(2, 0), (2, 5), (2, 6)],  # 0, 5, 6, 2, 4
    #     [(3, 4), (2, 'C')],
    #     [(3, 5), (3, 6), (1, 4)],
    #     [(3, 0), (3, 1), (3, 2)],  # 0, 1, 2, 4, 5, 6
    # ])  # cost 36165

    return graph
