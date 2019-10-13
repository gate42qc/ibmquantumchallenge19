from qiskit import QuantumRegister, ClassicalRegister, QuantumCircuit

from grover import grover
from init_state import uniform_superposition
from oracles import simple_oracle
from utils import run_and_print_results


def run_simple_grover():
    iter_count = 1
    state_size = 2
    state_register = QuantumRegister(state_size)
    ancilla_register = QuantumRegister(state_size-1)
    results_register = ClassicalRegister(state_size)
    qc = QuantumCircuit(state_register, ancilla_register, results_register)

    grover_instructions = grover(state_register, ancilla_register,
                                 uniform_superposition, simple_oracle, iter_count)

    qc.append(grover_instructions, state_register[:] + ancilla_register[:])
    qc.measure(state_register, results_register)

    return run_and_print_results(qc)


if __name__ == '__main__':
    results = run_simple_grover()


