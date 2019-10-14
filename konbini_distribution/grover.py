from typing import Callable
from qiskit import QuantumCircuit, QuantumRegister
from utils import flip_all

StateInitializerType = Callable[[int], QuantumCircuit]
# oracle(state_register_size, ancilla_register_size): QuantumCircuit
OracleType = Callable[[], QuantumCircuit]


def grover(state_register: QuantumRegister, ancilla_register: QuantumRegister, init_state: StateInitializerType,
           oracle: OracleType, iter_count: int):
    qc = QuantumCircuit(state_register, ancilla_register, name="Grover")
    target = ancilla_register[-1]

    # initialize the state
    init_instructions = init_state(len(state_register)).to_instruction()
    qc.append(init_instructions, state_register)

    # initialize the target qubit
    qc.x(target)
    qc.h(target)

    for i in range(iter_count):
        oracle_instructions = oracle()
        qc.append(oracle_instructions, state_register[:] + ancilla_register[:])

        qc.append(init_instructions.inverse(), state_register)
        # create_uniform_superposition(qc, state_register[:])
        flip_all(qc, state_register)
        qc.h(state_register[-1])
        qc.mct(state_register[:-1], state_register[-1], ancilla_register[:len(state_register) - 3])
        qc.h(state_register[-1])

        flip_all(qc, state_register)
        # create_uniform_superposition(qc, state_register[:])
        qc.append(init_instructions, state_register)

    # print("Grover part: \n", qc)

    return qc
