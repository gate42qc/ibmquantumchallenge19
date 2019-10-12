from qiskit import QuantumRegister
from qiskit import ClassicalRegister
from qiskit import QuantumCircuit

NUM_ITER = 5
EDGES = [(0, 1), (0, 2), (0, 3), (0, 7), (1, 3), 
         (1, 4), (1, 8), (2, 3), (2, 5), (2, 6), 
         (2, 7), (2, 9), (3, 4), (3, 5), (3, 6), 
         (3, 7), (4, 6), (4, 8), (5, 6), (5, 10), 
         (6, 10), (9, 10)]

def check_same_color(qc, q1, q2, q3, q4, a):
    qc.cx(q1, q3)
    qc.cx(q2, q4)
    qc.cx(q3, a)
    qc.cx(q4, a)
    qc.ccx(q3, q4, a)
    
def check_same_color_reverse(qc, q1, q2, q3, q4, a):
    qc.ccx(q3, q4, a)
    qc.cx(q4, a)
    qc.cx(q3, a)
    qc.cx(q2, q4)
    qc.cx(q1, q3)

def check_same_color_with_A(qc, q1, q2, a):
    qc.cx(q1, a)
    qc.cx(q2, a)
    qc.ccx(q1, q2, a)
    
def check_same_color_with_A_reverse(qc, q1, q2, a):
    qc.ccx(q1, q2, a)
    qc.cx(q2, a)
    qc.cx(q1, a)

def check_same_color_with_B(qc, q1, q2, a):
    qc.x(q2)
    qc.cx(q1, a)
    qc.cx(q2, a)
    qc.ccx(q1, q2, a)

def check_same_color_with_B_reverse(qc, q1, q2, a):
    qc.ccx(q1, q2, a)
    qc.cx(q2, a)
    qc.cx(q1, a)
    qc.x(q2)
    
def check_same_color_with_C(qc, q1, q2, a):
    qc.x(q1)
    qc.cx(q1, a)
    qc.cx(q2, a)
    qc.ccx(q1, q2, a)
    
def check_same_color_with_C_reverse(qc, q1, q2, a): 
    qc.ccx(q1, q2, a)
    qc.cx(q2, a)
    qc.cx(q1, a)
    qc.x(q1)

def check_same_color_with_D(qc, q1, q2, a):
    qc.x(q1)
    qc.x(q2)
    qc.cx(q1, a)
    qc.cx(q2, a)
    qc.ccx(q1, q2, a)
    
def check_same_color_with_D_reverse(qc, q1, q2, a):
    qc.ccx(q1, q2, a)
    qc.cx(q2, a)
    qc.cx(q1, a)
    qc.x(q2)
    qc.x(q1)



qdistricts = QuantumRegister(16, 'district')
qancilla = QuantumRegister(16, 'ancilla')
creg = ClassicalRegister(14)
qc = QuantumCircuit(qdistricts, qancilla, creg)

# prepare uniform superposition of all possible combinations.
qc.h(qdistricts[0:14])
qc.x(qdistricts[14])
qc.x(qancilla[15])
qc.h(qancilla[15])
qc.barrier()

for i in range(NUM_ITER):
    # create the oracle
    ##################################
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[6], qdistricts[7], qancilla[0])
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[12], qdistricts[13], qancilla[2])    
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[14], qdistricts[15], qancilla[3])
    check_same_color_with_A(qc, qdistricts[4], qdistricts[5], qancilla[4])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2], qancilla[3], qancilla[4]], qancilla[5], qancilla[12:15])
    
    check_same_color_with_A_reverse(qc, qdistricts[4], qdistricts[5], qancilla[4])
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[14], qdistricts[15], qancilla[3])
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[12], qdistricts[13], qancilla[2])
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[6], qdistricts[7], qancilla[0])
    #####################################
    
    ###################################
    check_same_color(qc, qdistricts[0], qdistricts[1], qdistricts[2], qdistricts[3], qancilla[0])
    check_same_color(qc, qdistricts[0], qdistricts[1], qdistricts[4], qdistricts[5], qancilla[1])
    check_same_color(qc, qdistricts[0], qdistricts[1], qdistricts[6], qdistricts[7], qancilla[2])
    check_same_color_with_A(qc, qdistricts[0], qdistricts[1], qancilla[3])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2], qancilla[3]], qancilla[6], qancilla[12:14])
    
    check_same_color_with_A_reverse(qc, qdistricts[0], qdistricts[1], qancilla[3])
    check_same_color_reverse(qc, qdistricts[0], qdistricts[1], qdistricts[6], qdistricts[7], qancilla[2])
    check_same_color_reverse(qc, qdistricts[0], qdistricts[1], qdistricts[4], qdistricts[5], qancilla[1])
    check_same_color_reverse(qc, qdistricts[0], qdistricts[1], qdistricts[2], qdistricts[3], qancilla[0])
    ############################
    
    ###########################
    check_same_color(qc, qdistricts[2], qdistricts[3], qdistricts[6], qdistricts[7], qancilla[0])
    check_same_color(qc, qdistricts[2], qdistricts[3], qdistricts[8], qdistricts[9], qancilla[1])
    check_same_color_with_B(qc, qdistricts[2], qdistricts[3], qancilla[2])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2]], qancilla[7], [qancilla[12]])
    
    check_same_color_with_B_reverse(qc, qdistricts[2], qdistricts[3], qancilla[2])
    check_same_color_reverse(qc, qdistricts[2], qdistricts[3], qdistricts[8], qdistricts[9], qancilla[1])
    check_same_color_reverse(qc, qdistricts[2], qdistricts[3], qdistricts[6], qdistricts[7], qancilla[0])
    ################################
    
    ##############################
    check_same_color(qc, qdistricts[6], qdistricts[7], qdistricts[8], qdistricts[9], qancilla[0])
    check_same_color(qc, qdistricts[6], qdistricts[7], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color(qc, qdistricts[6], qdistricts[7], qdistricts[12], qdistricts[13], qancilla[2])
    check_same_color_with_A(qc, qdistricts[6], qdistricts[7], qancilla[3])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2], qancilla[3]], qancilla[8], qancilla[12:14])
    
    check_same_color_with_A_reverse(qc, qdistricts[6], qdistricts[7], qancilla[3])
    check_same_color_reverse(qc, qdistricts[6], qdistricts[7], qdistricts[12], qdistricts[13], qancilla[2])
    check_same_color_reverse(qc, qdistricts[6], qdistricts[7], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color_reverse(qc, qdistricts[6], qdistricts[7], qdistricts[8], qdistricts[9], qancilla[0])
    #########################################################
    
    ########################################
    check_same_color(qc, qdistricts[8], qdistricts[9], qdistricts[12], qdistricts[13], qancilla[0])
    check_same_color_with_B(qc, qdistricts[8], qdistricts[9], qancilla[1])
    
    qc.ccx(qancilla[0], qancilla[1], qancilla[9])
    
    check_same_color_with_B_reverse(qc, qdistricts[8], qdistricts[9], qancilla[1])
    check_same_color_reverse(qc, qdistricts[8], qdistricts[9], qdistricts[12], qdistricts[13], qancilla[0])
    ########################################
    
    ########################################
    check_same_color(qc, qdistricts[10], qdistricts[11], qdistricts[12], qdistricts[13], qancilla[0])
    check_same_color_with_D(qc, qdistricts[10], qdistricts[11], qancilla[1])
    
    qc.ccx(qancilla[0], qancilla[1], qancilla[10])
    
    check_same_color_with_D_reverse(qc, qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color_reverse(qc, qdistricts[10], qdistricts[11], qdistricts[12], qdistricts[13], qancilla[0])
    ########################################
    
    ########################################
    check_same_color_with_D(qc, qdistricts[12], qdistricts[13], qancilla[0])
    
    qc.cx(qancilla[0], qancilla[11])
    
    check_same_color_with_D_reverse(qc, qdistricts[12], qdistricts[13], qancilla[0])
    ########################################
    
    
    qc.mct(qancilla[5:12], qancilla[15], qancilla[0:5])
    
    
    ########################################
    
    
    ####################################
    ######FULL REVERSE##################
    ####################################
    check_same_color_with_D(qc, qdistricts[12], qdistricts[13], qancilla[0])
    
    qc.cx(qancilla[0], qancilla[11])
    
    check_same_color_with_D_reverse(qc, qdistricts[12], qdistricts[13], qancilla[0])
    ########################################
    
    ########################################
    check_same_color(qc, qdistricts[10], qdistricts[11], qdistricts[12], qdistricts[13], qancilla[0])
    check_same_color_with_D(qc, qdistricts[10], qdistricts[11], qancilla[1])
    
    qc.ccx(qancilla[0], qancilla[1], qancilla[10])
    
    check_same_color_with_D_reverse(qc, qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color_reverse(qc, qdistricts[10], qdistricts[11], qdistricts[12], qdistricts[13], qancilla[0])
    ########################################
    
    ########################################
    check_same_color(qc, qdistricts[8], qdistricts[9], qdistricts[12], qdistricts[13], qancilla[0])
    check_same_color_with_B(qc, qdistricts[8], qdistricts[9], qancilla[1])
    
    qc.ccx(qancilla[0], qancilla[1], qancilla[9])
    
    check_same_color_with_B_reverse(qc, qdistricts[8], qdistricts[9], qancilla[1])
    check_same_color_reverse(qc, qdistricts[8], qdistricts[9], qdistricts[12], qdistricts[13], qancilla[0])
    ########################################
    
    #########################################################
    check_same_color(qc, qdistricts[6], qdistricts[7], qdistricts[8], qdistricts[9], qancilla[0])
    check_same_color(qc, qdistricts[6], qdistricts[7], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color(qc, qdistricts[6], qdistricts[7], qdistricts[12], qdistricts[13], qancilla[2])
    check_same_color_with_A(qc, qdistricts[6], qdistricts[7], qancilla[3])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2], qancilla[3]], qancilla[8], qancilla[12:14])
    
    check_same_color_with_A_reverse(qc, qdistricts[6], qdistricts[7], qancilla[3])
    check_same_color_reverse(qc, qdistricts[6], qdistricts[7], qdistricts[12], qdistricts[13], qancilla[2])
    check_same_color_reverse(qc, qdistricts[6], qdistricts[7], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color_reverse(qc, qdistricts[6], qdistricts[7], qdistricts[8], qdistricts[9], qancilla[0])
    ##############################
    
    ################################
    check_same_color(qc, qdistricts[2], qdistricts[3], qdistricts[6], qdistricts[7], qancilla[0])
    check_same_color(qc, qdistricts[2], qdistricts[3], qdistricts[8], qdistricts[9], qancilla[1])
    check_same_color_with_B(qc, qdistricts[2], qdistricts[3], qancilla[2])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2]], qancilla[7], [qancilla[12]])
    
    check_same_color_with_B_reverse(qc, qdistricts[2], qdistricts[3], qancilla[2])
    check_same_color_reverse(qc, qdistricts[2], qdistricts[3], qdistricts[8], qdistricts[9], qancilla[1])
    check_same_color_reverse(qc, qdistricts[2], qdistricts[3], qdistricts[6], qdistricts[7], qancilla[0])
    ###########################
    
    ############################
    check_same_color(qc, qdistricts[0], qdistricts[1], qdistricts[2], qdistricts[3], qancilla[0])
    check_same_color(qc, qdistricts[0], qdistricts[1], qdistricts[4], qdistricts[5], qancilla[1])
    check_same_color(qc, qdistricts[0], qdistricts[1], qdistricts[6], qdistricts[7], qancilla[2])
    check_same_color_with_A(qc, qdistricts[0], qdistricts[1], qancilla[3])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2], qancilla[3]], qancilla[6], qancilla[12:14])
    
    check_same_color_with_A_reverse(qc, qdistricts[0], qdistricts[1], qancilla[3])
    check_same_color_reverse(qc, qdistricts[0], qdistricts[1], qdistricts[6], qdistricts[7], qancilla[2])
    check_same_color_reverse(qc, qdistricts[0], qdistricts[1], qdistricts[4], qdistricts[5], qancilla[1])
    check_same_color_reverse(qc, qdistricts[0], qdistricts[1], qdistricts[2], qdistricts[3], qancilla[0])
    ###################################
    
    #####################################
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[6], qdistricts[7], qancilla[0])
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[12], qdistricts[13], qancilla[2])
    check_same_color(qc, qdistricts[4], qdistricts[5], qdistricts[14], qdistricts[15], qancilla[3])
    check_same_color_with_A(qc, qdistricts[4], qdistricts[5], qancilla[4])
    
    qc.mct([qancilla[0], qancilla[1], qancilla[2], qancilla[3], qancilla[4]], qancilla[5], qancilla[12:15])
    
    check_same_color_with_A_reverse(qc, qdistricts[4], qdistricts[5], qancilla[4])
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[14], qdistricts[15], qancilla[3])
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[12], qdistricts[13], qancilla[2])    
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[10], qdistricts[11], qancilla[1])
    check_same_color_reverse(qc, qdistricts[4], qdistricts[5], qdistricts[6], qdistricts[7], qancilla[0])

    
    ####################################
    ######FULL REVERSE END##############
    ####################################
    
    # inversion about mean
    qc.h(qdistricts)
    qc.x(qdistricts)
    
    qc.h(qdistricts[13])
    qc.mct(qdistricts[0:13], qdistricts[13], qancilla[0:11])
    qc.h(qdistricts[13])
    
    qc.x(qdistricts)
    qc.h(qdistricts)

qc.barrier()

# measurements
for i in range(14):
    qc.measure(qdistricts[i], creg[i])

#qc.draw(output='mpl')