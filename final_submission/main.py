from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit
from coloring_oracle import get_konbini_oracle
from grover import grover
from graph import Graph


def run_coloring_grover(graph: Graph, iter_count: int):
    state_size = len(graph.vertices) * graph.color_bit_length
    state_register = QuantumRegister(state_size)
    ancilla_register = QuantumRegister(graph.get_ancilla_size_needed())
    results_register = ClassicalRegister(state_size)
    qc = QuantumCircuit(state_register, ancilla_register, results_register)

    grover_instructions = grover(state_register, ancilla_register,
                                 graph.get_all_possible_state_preparing_circuit_initializer(),
                                 get_konbini_oracle(graph), iter_count)

    qc.append(grover_instructions, state_register[:] + ancilla_register[:])

    finalizer_circuit = graph.get_state_finalization_circuit()
    qc.append(finalizer_circuit, state_register[:])

    qc.measure(state_register, results_register)

    return qc
