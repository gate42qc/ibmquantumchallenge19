from qiskit import QuantumCircuit, QuantumRegister
from graph import Graph
from grover import OracleType
from utils import get_check_same_color_circuit


def get_konbini_oracle(graph: Graph) -> OracleType:
    def get_all_edges_comparing_circuit(state_register_size: int, ancilla_register_size: int):
        state_register = QuantumRegister(state_register_size)

        group_edge_results = QuantumRegister(graph.largest_group_size)
        all_group_results = QuantumRegister(len(graph.groups))
        mct_ancilla = QuantumRegister(len(group_edge_results) - 2)
        target_register = QuantumRegister(1)

        qc = QuantumCircuit(state_register, group_edge_results, all_group_results, mct_ancilla, target_register,
                            name="Edge comparison")

        for group_index, group in enumerate(graph.groups):
            vertex1, connected_vertices = group
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

            qc.mct(
                group_edge_results[:len(connected_vertices)],
                all_group_results[group_index],
                mct_ancilla[:]
            )

            for edge_index, vertex2 in enumerate(connected_vertices):
                if vertex2.is_external():
                    additional_restrictions_circuit = graph.get_additional_restrictions_circuit(vertex1, vertex2)

                    vertex_registers = vertex1.get_qubits(state_register)
                    check_registers = vertex_registers + [group_edge_results[edge_index]]
                    qc.append(additional_restrictions_circuit.inverse(), check_registers)
                else:
                    check_same_color_circuit = get_check_same_color_circuit(graph.color_bit_length)

                    vertex_registers = vertex1.get_qubits(state_register) + vertex2.get_qubits(state_register)
                    check_registers = vertex_registers + [group_edge_results[edge_index]]
                    qc.append(check_same_color_circuit.inverse(), check_registers)

        return qc

    def oracle(state_register_size: int, ancilla_register_size: int) -> QuantumCircuit:
        state_register = QuantumRegister(state_register_size)
        group_edge_results = QuantumRegister(graph.largest_group_size)
        all_group_results = QuantumRegister(len(graph.groups))
        mct_ancilla = QuantumRegister(len(group_edge_results) - 2)
        target_register = QuantumRegister(1)
        target = target_register[0]
        all_ancilla_qubits = group_edge_results[:] + all_group_results[:] + mct_ancilla[:] + target_register[:]

        # ancilla_size = len(ancilla_1_register) + len(ancilla_2_register) + 1
        qc = QuantumCircuit(state_register, group_edge_results, all_group_results, mct_ancilla, target_register,
                            name="Oracle")

        # todo: fix register sharing
        compare_all_vertices_circuit = get_all_edges_comparing_circuit(state_register_size, 1)
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

