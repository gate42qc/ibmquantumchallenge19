from typing import List

from qiskit import QuantumCircuit, QuantumRegister
from graph import Graph
from grover import OracleType
from utils import get_check_same_color_circuit

from konbini_distribution.graph import Vertex


def get_konbini_oracle(graph: Graph) -> OracleType:
    state_register = QuantumRegister(len(graph.vertices) * graph.color_bit_length)

    group_edge_results = QuantumRegister(graph.largest_group_size)
    all_group_results = QuantumRegister(len(graph.groups))
    mct_ancilla = QuantumRegister(len(group_edge_results) - 2)
    target_register = QuantumRegister(1)

    def get_all_edges_comparing_circuit(vertex1: Vertex, connected_vertices: List[Vertex]):
        qc = QuantumCircuit(state_register, group_edge_results, all_group_results, mct_ancilla, target_register,
                            name="Edge comparison")

        for edge_index, vertex2 in enumerate(connected_vertices):
            if vertex2.is_external():
                additional_restrictions_circuit = graph.get_additional_restrictions_circuit(vertex1, vertex2)

                vertex_registers = vertex1.get_qubits(state_register)
                check_registers = vertex_registers + [group_edge_results[edge_index]]
                qc.append(additional_restrictions_circuit, check_registers)
            else:
                check_same_color_circuit = get_check_same_color_circuit(graph.color_bit_length)

                vertex_registers = vertex1.get_qubits(state_register) + vertex2.get_qubits(state_register)
                check_registers = vertex_registers + [group_edge_results[edge_index]]
                qc.append(check_same_color_circuit, check_registers)

        return qc

    def get_all_groups_comparing_circuit():
        all_registers = state_register[:] + group_edge_results[:] + all_group_results[:] + mct_ancilla[:] + target_register[:]

        qc = QuantumCircuit(state_register, group_edge_results, all_group_results, mct_ancilla, target_register,
                            name="Group comparison")

        for group_index, group in enumerate(graph.groups):
            vertex1, connected_vertices = group
            edges_comparing_circuit = get_all_edges_comparing_circuit(vertex1, connected_vertices)

            qc.append(edges_comparing_circuit, all_registers)

            qc.mct(
                group_edge_results[:len(connected_vertices)],
                all_group_results[group_index],
                mct_ancilla[:]
            )

            qc.append(edges_comparing_circuit.inverse(), all_registers)

        return qc

    def oracle() -> QuantumCircuit:
        target = target_register[0]
        all_ancilla_qubits = group_edge_results[:] + all_group_results[:] + mct_ancilla[:] + target_register[:]

        qc = QuantumCircuit(state_register, group_edge_results, all_group_results, mct_ancilla, target_register,
                            name="Oracle")

        compare_all_vertices_circuit = get_all_groups_comparing_circuit()
        apply_to_register = state_register[:] + all_ancilla_qubits

        qc.append(compare_all_vertices_circuit, apply_to_register)

        qc.mct(
            all_group_results,
            target,
            group_edge_results
        )

        qc.append(compare_all_vertices_circuit.inverse(), apply_to_register)

        return qc

    return oracle

