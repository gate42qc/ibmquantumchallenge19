import operator
from typing import List
from collections import OrderedDict

from qiskit import QuantumCircuit, Aer, execute, QuantumRegister
from qiskit.circuit import Qubit

from qiskit.transpiler import PassManager
from qiskit.transpiler.passes import Unroller
from qiskit import IBMQ

from not_n_cirqs import get_not_00_state, get_not_01_state, get_not_10_state, get_not_11_state


def create_uniform_superposition(circuit: QuantumCircuit, register: List[Qubit]):
    for qubit in register:
        circuit.h(qubit)


def flip_all(circuit: QuantumCircuit, register: List[Qubit]):
    for qubit in register:
        circuit.x(qubit)


def simulate_locally(circuit):
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(circuit, simulator, shots=1000)
    result = job.result()
    counts = result.get_counts(circuit)
    sorted_counts = sorted(counts.items(), key=operator.itemgetter(1))[::-1]
    print("\nTotal count for 00 and 11 are:", sorted_counts)
    return counts


def get_check_same_color_circuit(color_bitstring_size: int) -> QuantumCircuit:
    vertex1 = QuantumRegister(color_bitstring_size)
    vertex2 = QuantumRegister(color_bitstring_size)
    target_register = QuantumRegister(1)
    target = target_register[0]
    qc = QuantumCircuit(vertex1, vertex2, target_register)
    if len(vertex1) != len(vertex2):
        raise ValueError()

    for i in range(len(vertex1)):
        qc.cx(vertex1[i], vertex2[i])

    for i in range(len(vertex2)):
        qc.x(vertex2[i])

    qc.ccx(*vertex2, target)
    qc.x(target)

    return qc


def run_and_print_results(qc: QuantumCircuit):
    simulator = Aer.get_backend('qasm_simulator')
    job = execute(qc, simulator, shots=1000)
    result = job.result()
    counts = result.get_counts(qc)
    sorted_counts = OrderedDict(sorted(counts.items(), key=operator.itemgetter(1))[::-1])

    print([(k[::-1], c) for k, c in sorted_counts.items()])

    return sorted_counts


def run_and_print_results_state(qc: QuantumCircuit):
    simulator = Aer.get_backend('statevector_simulator')
    job = execute(qc, simulator)
    result = job.result()
    state_vector = result.get_statevector()
    print(state_vector)

    return state_vector


def get_cost(qc: QuantumCircuit) -> int:
    pass_ = Unroller(['u3', 'cx'])
    pm = PassManager(pass_)
    new_circuit = pm.run(qc)
    # new_circuit.draw(output='mpl')
    counts = new_circuit.count_ops()
    cost = counts["u3"] + 10 * counts['cx']

    print(counts)

    return cost


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


def submit_job(qc: QuantumCircuit):
    provider = IBMQ.load_account()
    backend = provider.get_backend('ibmq_qasm_simulator')
    job = execute(qc, backend=backend, shots=8000, seed_simulator=12345, backend_options={"fusion_enable": True})
    print(job)
    return job


def get_job_result(job_id: str):
    provider = IBMQ.load_account()
    backend = provider.get_backend('ibmq_qasm_simulator')
    job = backend.retrieve_job(job_id)

    return job.result()


