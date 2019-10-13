from typing import List, Tuple, Union

from qiskit import QuantumRegister, QuantumCircuit
from qiskit.circuit import Qubit

from grover import StateInitializerType
from utils import create_uniform_superposition, get_superposition_without_state_circuit

KONBINI_NAMES = ['A', 'B', 'C', 'D']
COLORS = ['RED', 'BLUE', 'GREEN', 'YELLOW']


class Konbini:
    name: str
    encoding: str
    color: str

    def __init__(self, name: str, color: str, encoding: str):
        self.name = name
        self.encoding = encoding
        self.color = color

    def __eq__(self, other: 'Konbini'):
        return other.encoding == self.encoding

    @staticmethod
    def get_by_name(name):
        number = KONBINI_NAMES.index(name)
        return Konbini(name, COLORS[number], "{0:02b}".format(number))

    def __str__(self):
        return f"Konbini {self.name}"

    def __repr__(self):
        return self.__str__()


class Vertex:
    graph: 'Graph'
    number: Union[int, None]
    konbini: Konbini
    neighbours: List['Vertex']

    def __init__(self, graph: 'Graph', number: Union[int, None]):
        self.graph = graph
        self.number = number
        self.konbini = None
        self.neighbours = []

    def is_external(self) -> bool:
        return self.number is None

    def add_neighbour(self, neighbour: 'Vertex'):
        self.neighbours.append(neighbour)

    def get_qubits(self, state_register: Union[QuantumRegister, List[Qubit]]) -> List[Qubit]:
        return state_register[self.number * self.graph.color_bit_length:self.number * self.graph.color_bit_length + self.graph.color_bit_length]

    def __str__(self):
        return f"Vertex {self.number}"

    def __repr__(self):
        return self.__str__()

    def __eq__(self, other: 'Vertex'):
        return other.number == self.number


class Graph:
    color_bit_length: int = 2
    largest_number_of_neighbours: int = 0
    largest_group_size: int = 0
    vertices: List[Vertex]
    edges: List[Tuple[Vertex, Vertex]]
    external_edges: List[Tuple[Konbini, Vertex]]
    groups: List[Tuple[Vertex, List[Vertex]]]

    def __init__(self, number_of_vertices: int, edges: List[Tuple[int, int]],
                 external_edges: List[Tuple[Konbini, int]] = None):
        self.vertices = [Vertex(self, i) for i in range(number_of_vertices)]
        self.edges = []
        self.groups = []

        for start, end in edges:
            self._add_edge(start, end)

        if external_edges is None:
            external_edges = []
        self.external_edges = []

        for konbini, index in external_edges:
            self._add_external_edge(konbini, index)

        for vertex in self.vertices:
            if len(vertex.neighbours) > self.largest_number_of_neighbours:
                self.largest_number_of_neighbours = len(vertex.neighbours)

            if len(vertex.neighbours) > 0:
                self.groups.append((vertex, [neighbour for neighbour in vertex.neighbours]))

        self.largest_group_size = self.largest_number_of_neighbours

    def _add_edge(self, start: int, end: int):
        if end < start:
            tmp = end
            end = start
            start = tmp

        self.vertices[start].add_neighbour(self.vertices[end])
        self.edges.append((self.vertices[start], self.vertices[end]))

    def _add_external_edge(self, konbini: Konbini, index: int):
        if konbini.encoding == "00":
            external_vertex = Vertex(self, None)
            external_vertex.konbini = konbini
            self.vertices[index].add_neighbour(external_vertex)
            self.edges.append((self.vertices[index], external_vertex))
        else:
            self.external_edges.append((konbini, self.vertices[index]))

    def get_all_possible_state_preparing_circuit_initializer(self) -> StateInitializerType:
        def initializer(size: int) -> QuantumCircuit:
            state_register = QuantumRegister(size)
            qc = QuantumCircuit(state_register, name="State Init")
            vertices_initialized = [False for i in range(len(self.vertices))]

            for konbini, vertex in self.external_edges:
                init_state_circuit = get_superposition_without_state_circuit(konbini.encoding)
                qc.append(init_state_circuit, vertex.get_qubits(state_register))
                vertices_initialized[vertex.number] = True

            for vertex in self.vertices:
                if not vertices_initialized[vertex.number]:
                    create_uniform_superposition(qc, vertex.get_qubits(state_register))

            # print("Graph state init: \n", qc)

            return qc

        return initializer

    def get_additional_restrictions_circuit(self, vertex: Vertex, external_vertex: Vertex) -> QuantumCircuit:
        if not external_vertex.is_external() or external_vertex.konbini.encoding != "00":
            raise ValueError()

        register = QuantumRegister(self.color_bit_length)
        target_register = QuantumRegister(1)
        target = target_register[0]
        qc = QuantumCircuit(register, target_register)
        qc.x(register)
        qc.ccx(*register, target)
        qc.x(target)

        return qc

    def get_ancilla_size_needed(self):
        group_edge_results_size = self.largest_group_size
        all_group_results_size = len(self.groups)
        mct_ancilla_size = group_edge_results_size - 2
        target_register_size = 1
        return group_edge_results_size + all_group_results_size + mct_ancilla_size + target_register_size

    def color(self, color_bitstring: str):
        for i in range(len(self.vertices)):
            color_code = color_bitstring[i*self.color_bit_length:i*self.color_bit_length + self.color_bit_length]
            color_index = int(color_code, 2)

            self.vertices[i].konbini = Konbini(KONBINI_NAMES[color_index], COLORS[color_index], color_code)

    def is_coloring_valid(self):
        for start, end in self.edges:
            if start.konbini == end.konbini:
                return False

        for konbini, vertex in self.external_edges:
            if vertex.konbini == konbini:
                return False

        return True

    def get_colored(self, color_bitstring: str):
        new_graph = Graph(len(self.vertices),
                          [(start.number, end.number) for start, end in self.edges if not end.is_external()],
                          [(end.konbini, start.number) for start, end in self.edges if end.is_external()] + [
                              (konbini, vertex.number) for konbini, vertex in self.external_edges
                          ],
                          )
        new_graph.color(color_bitstring)
        return new_graph
