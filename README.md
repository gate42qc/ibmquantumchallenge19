# IBM-Quantum-Challenge-2019

This is our solution to the final challenge of the IBM Quantum Challenge 2019 Hackathon.
You can read about the hackathon [here](https://quantumchallenge19.com/).

# What was the final challenge about?

Zed City is a newly established (fictitious) municipality in Tokyo and is made up of 11 districts. <br/> 
Four convenience store ( _konbini_ ) chains A, B, C and D have each established their first store in this new city in non-overlapping districts.
The map (or graph) below shows the 11 districts of Zed City and which district has a konbini already.

Since this map looks different from a conventional one, let us explain how you should look at it once more just in case.<br/>
If you count the number of nodes in this map (or graph), you'll notice that there are 11 of them. So, you should be able to tell that each node in this map (or graph) represents one of the 11 districts of Zed city. The colored nodes are the districts that have konbinis already with each color representing a different konbini chain. In this graph, konbini chain A is represented in Red, B in Blue, C in Yellow and D in Green. Next, you should take notice of the edges that connect these nodes. Any node (district) connected to each other by an edge means that they are districts adjacent to each other.
<img src="./older_Submissions/tokyo_map_pic.png" width="700">
As the mayor of Zed City, you want to establish konbinis in the rest of the districts that still don't have one yet.<br/>
Upon your request, all four konbini chains discussed with each other and agreed to establish their konbinis in Zed City under the following two conditions:

**-Only one konbini is allowed in one district.**<br/>
**-No two adjacent districts can have konbinis from the same chain.**<br/>

Can you come up with a plan that satisfies the above conditions? (For details of the problem, visit [final challenge](https://github.com/quantum-challenge/2019/tree/master/problems/final)).

Answers and comments by judges: https://github.com/quantum-challenge/2019/blob/master/problems/final/answer_and_comment_by_judges_en.ipynb.
Top 10 submissions: https://github.com/quantum-challenge/2019/tree/master/top%20ten%20submissions.

# Our solution

The challenge problem can be represented as a graph coloring problem and can be solved with grover algorithm.

So let's represent the Zed city as a graph with:

__Vertices:__ \[A, 0, 1, B, 2, 3, 4, C, 5, 6, D\]

and 

__Edges:__ \[(A,0), (A,2), (A,3), (0,1), (0,2), (0,3), (1,B), (1,3), (1,4), (B,4), (2,3), (2,5), (2,6), (2,C), (3,4), (3,5), (3,6), (4,6), (C, D), (5,6), (5,D), (6,D)\]

Colors of vertexes A, B, C and D are fixed and can be though of as external constrains on a smaller graph without this edges so we will not represent those edges in our graph.

We will use two qubits to represent each district. The state of the pair of qubits encodes the konbini code. E.g. if the pair of qubits representing the 4th district is `10`, then there is a konbini store from the chain C in this district.

Then algorithm would look like this: 

|**Step**  |**Content** |
| ---     |--- |
| Step1 |Create a superposition of inputs |
| Step2 |Build an oracle according to the constraints of the problem |
| Step3 |Diffusion |
| Step4 |Measurement |

According to the challenge statement, we are given a 32-qubit machine (a simulator), so we have an upper bound on the number of qubits we can use to solve the problem. Here is a short description of how we have used the 32 qubits of the given machine for our solution.

| Qubit(s) | Type | Usage   |
|------|------|------|
|  \[0-13\]  | state | to represent the konbinis in districts 0 to 6 |
| \[14-19\] | ancilla | to store results of color check within an edge group \* |
| \[20-22\] | ancilla | to store the combined result for each group of edges |
| \[23-26\] | ancilla | ancilla qubits for _mct_ gates used in the circuit \*\*|
| 27 | ancilla | the target qubit for oracle phase flip |

\* In our oracle we process the graph edges in groups, so that we can fit in the 32 qubit limit of the challenge.

\*\* The _mct_ gate with $N$ controls ($N > 2$) requires at least $N-2$ ancila qubits.

You can read more detailed explanation of our solution [here](https://github.com/quantum-challenge/2019/blob/master/top%20ten%20submissions/Gate42/Final%20challenge%20write%20up%20-%20Gate42.ipynb).

# Usage

To use our code for other graph coloring problems you can just create an instance of the Graph class from graph.py
and use the run_coloring_grover function from main.py which will return a qiskit QuantumCircuit object which can be run
as any other QuantumCircuit.

Examples of usage can be found in tests.py file.

Code for running the algorithm with actual challenge graph can be found in job_submission Jupyter notebook file.

