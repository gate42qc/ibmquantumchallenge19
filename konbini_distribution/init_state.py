from qiskit import QuantumCircuit, QuantumRegister


def uniform_superposition(state_size: int) -> QuantumCircuit:
    register = QuantumRegister(state_size)
    qc = QuantumCircuit(register)

    qc.h(register)

    return qc
