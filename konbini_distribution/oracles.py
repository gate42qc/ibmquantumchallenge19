from qiskit import QuantumRegister, QuantumCircuit


def simple_oracle(state_register_size: int, ancilla_register_size: int) -> QuantumCircuit:
    state_register = QuantumRegister(state_register_size)
    ancilla_register = QuantumRegister(ancilla_register_size)
    qc = QuantumCircuit(state_register, ancilla_register)

    qc.mct(state_register, ancilla_register[-1],  ancilla_register[:len(state_register)-2])

    return qc


