from math import pi

from qiskit import QuantumCircuit, QuantumRegister


def get_not_00_state():
    """
    Initializes a two-qubit state into a superposition state where all participating states have equal amplitudes,
    except |00>, which has amplitude equal to zero.
    """
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_A')
    qc.ry(pi - 1.910634, 0)
    qc.x(1)
    qc.cx(0, 1)
    qc.ch(1, 0)

    return qc


def get_not_01_state():
    """
    Initializes a two-qubit state into a superposition state where all participating states have equal amplitudes,
    except |01>, which has amplitude equal to zero.
    """
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_B')
    qc.ry(1.910634, 0)
    qc.ch(0, 1)

    return qc


def get_not_10_state():
    """
    Initializes a two-qubit state into a superposition state where all participating states have equal amplitudes,
    except |10>, which has amplitude equal to zero.
    """
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_C')
    qc.ry(1.910634, 1)
    qc.ch(1, 0)

    return qc


def get_not_11_state():
    """
    Initializes a two-qubit state into a superposition state where all participating states have equal amplitudes,
    except |10>, which has amplitude equal to zero.
    """
    register = QuantumRegister(2)
    qc = QuantumCircuit(register, name='not_D')
    qc.ry(pi - 1.910634, 0)
    qc.x(0)
    qc.ch(0, 1)
    qc.x(0)

    return qc


def get_superposition_without_state_circuit(state: str):
    if state == "00":
        return get_not_00_state()
    elif state == "01":
        return get_not_01_state()
    elif state == "10":
        return get_not_10_state()
    elif state == "11":
        return get_not_11_state()

    raise ValueError()
