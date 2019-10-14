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

    for i in range(color_bitstring_size):
        qc.cx(vertex1[i], vertex2[i])

    for i in range(color_bitstring_size):
        qc.x(vertex2[i])

    qc.ccx(*vertex2, target)
    qc.x(target)

    return qc


def get_check_same_color_circuit_1(color_bitstring_size: int) -> QuantumCircuit:
    vertex1 = QuantumRegister(color_bitstring_size)
    vertex2 = QuantumRegister(color_bitstring_size)
    qc = QuantumCircuit(vertex1, vertex2)
    if len(vertex1) != len(vertex2):
        raise ValueError()

    for i in range(color_bitstring_size):
        qc.cx(vertex1[i], vertex2[i])

    for i in range(color_bitstring_size):
        qc.x(vertex2[i])

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


def generate_contest_submission_file(qc, results):
    # Input your quantum circuit
    circuit = qc
    # Input your result of the execute(groverCircuit, backend=backend, shots=shots).result()
    results = results
    count = results.get_counts()
    # Provide your team name
    name = 'Gate42'
    # Please indicate the number of times you have made a submission so far.
    # For example, if it's your 1st time to submit your answer, write 1. If it's your 5th time to submit your answer, write 5.
    times = '4'

    import json
    from qiskit.transpiler import PassManager
    from qiskit.transpiler.passes import Unroller

    # Unroll the circuit
    pass_ = Unroller(['u3', 'cx'])
    pm = PassManager(pass_)
    new_circuit = pm.run(circuit)

    # obtain gates
    gates = new_circuit.count_ops()

    # sort count
    count_sorted = sorted(count.items(), key=lambda x: x[1], reverse=True)

    # collect answers with Top 9 probability
    ans_list = count_sorted[0:9]

    # reverse ans_list
    ans_reversed = []
    for i in ans_list:
        ans_temp = [i[0][::-1], i[1]]
        ans_reversed.append(ans_temp)

    # convert each 2 bits into corresponding color. Add node0(0),node3(1),node8(2) and node11(3)
    ans_shaped = []
    for j in ans_reversed:
        ans_temp = j[0]
        nodeA = 0
        node0 = int(ans_temp[0] + ans_temp[1], 2)
        node1 = int(ans_temp[2] + ans_temp[3], 2)
        nodeB = 1
        node2 = int(ans_temp[4] + ans_temp[5], 2)
        node3 = int(ans_temp[6] + ans_temp[7], 2)
        node4 = int(ans_temp[8] + ans_temp[9], 2)
        nodeC = 2
        node5 = int(ans_temp[10] + ans_temp[11], 2)
        node6 = int(ans_temp[12] + ans_temp[13], 2)
        nodeD = 3
        nodes_color = str(nodeA) + str(node0) + str(node1) + str(nodeB) + str(node2) + str(node3) + str(node4) + str(
            nodeC) + str(node5) + str(node6) + str(nodeD)
        ans_shaped.append([nodes_color, j[1]])

    # write the result into '[your name]_final_output.txt'
    filename = name + '_' + times + '_final_output.txt'
    dct = {'ans': ans_shaped, 'costs': gates}
    with open(filename, 'w') as f:
        json.dump(dct, f)
