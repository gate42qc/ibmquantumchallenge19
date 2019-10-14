from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

from graph_coloring import get_konbini_oracle
from grover import grover
from utils import run_and_print_results, run_and_print_results_state
from graph import Graph, Konbini

from graph_examples import get_5_vertex_graph, get_4_vertex_graph


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


def test_state_init(graph: Graph):
    state_size = len(graph.vertices) * graph.color_bit_length
    state_register = QuantumRegister(state_size)
    results_register = ClassicalRegister(state_size)
    qc = QuantumCircuit(state_register, results_register)
    init_instructions = graph.get_all_possible_state_preparing_circuit_initializer()(len(state_register)).to_instruction()
    qc.append(init_instructions, state_register)
    qc.append(init_instructions.inverse(), state_register)

    # qc.measure(state_register, results_register)

    return run_and_print_results_state(qc)


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
