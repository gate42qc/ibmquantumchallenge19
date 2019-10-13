from qiskit import QuantumRegister, QuantumCircuit

from grover import OracleType


def get_simple_oracle(state_register_size: int) -> OracleType:
    def simple_oracle() -> QuantumCircuit:
        state_register = QuantumRegister(state_register_size)
        ancilla_register = QuantumRegister(state_register_size - 1)
        qc = QuantumCircuit(state_register, ancilla_register)

        qc.mct(state_register, ancilla_register[-1],  ancilla_register[:len(state_register)-2])

        return qc

    return simple_oracle


