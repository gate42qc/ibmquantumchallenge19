from math import pi

from qiskit import QuantumCircuit, QuantumRegister


def get_not_00_state():
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_A')
    qc.ry(pi - 1.910634, 0)
    qc.x(1)
    qc.cx(0, 1)
    qc.ch(1, 0)

    return qc


def get_not_01_state():
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_B')
    qc.ry(1.910634, 0)
    qc.ch(0, 1)

    return qc


def get_not_10_state():
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_C')
    qc.ry(1.910634, 1)
    qc.ch(1, 0)

    return qc


def get_not_11_state():
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_D')
    qc.ry(pi - 1.910634, 0)
    qc.x(0)
    qc.ch(0, 1)
    qc.x(0)

    return qc

