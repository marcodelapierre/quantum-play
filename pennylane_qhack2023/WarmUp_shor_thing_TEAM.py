import json
import pennylane as qml
import pennylane.numpy as np

n_qubits = 9
dev = qml.device("default.qubit", wires=n_qubits)
error_dict = {0: 'PauliX', 1: 'PauliY', 2: 'PauliZ'}

def error(error_key, qubit):
    """Defines the error that is induced in the circuit.

    Args:
        error_key (int): An integer associated to the type of error (Pauli X, Y, or Z)
        qubit (int): The qubit that the error occurs on.
    """
    getattr(qml, error_dict[error_key])(qubit)

@qml.qnode(dev)
def shor(state, error_key, qubit):
    """A circuit defining Shor's code for error correction.

    Args:
        state (list(float)): The quantum state of the first qubit in the circuit.
        error_key (int): An integer associated to the type of error (Pauli X, Y, or Z)
        qubit (int): The qubit that the error occurs on.

    Returns:
        (list(float)): The expectation value of the Pauli Z operator on every qubit.
    """
    qml.QubitStateVector(np.array(state), wires=0)



    # Put your code here #
    # apply the cnots
    cnotpairs=[[0,3], [0,6]]
    for w in cnotpairs:
        qml.CNOT(wires=w)
    # order matters but these are the wires which all have H gates applied at the same time
    for w in [0,3,6]:
        qml.Hadamard(w)
    for i in range(2):
        cnotpairs=[[0,1], [3,4], [6,7]]
        for w in cnotpairs:
            qml.CNOT(wires=w)
        cnotpairs=[[0,2], [3,5], [6,8]]
        for w in cnotpairs:
            qml.CNOT(wires=w)
        if i==0:
            error(error_key, qubit)
    toffoliset = [[1,2,0], [5,4,3], [8,7,6]]
    for w in toffoliset:
        qml.Toffoli(w)
    for w in [0,3,6]:
        qml.Hadamard(w)
    qml.CNOT([0,3])
    qml.CNOT([0,6])
    qml.Toffoli([6,3,0])

    # Put your code here #
    return [qml.expval(qml.PauliZ(w)) for w in range(9)]



# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    state, error_key, qubit = json.loads(test_case_input)
    output = shor(state, error_key, qubit).tolist()

    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)

    assert np.allclose(solution_output, expected_output, rtol=1e-4)

test_cases = [['[[0, 1], 0, 3]', '[-1.0,  1.0,  1.0,  1.0, -1.0, -1.0,  1.0,  1.0,  1.0]']]

for i, (input_, expected_output) in enumerate(test_cases):
    print(f"Running test case {i} with input '{input_}'...")

    try:
        output = run(input_)

    except Exception as exc:
        print(f"Runtime Error. {exc}")

    else:
        if message := check(output, expected_output):
            print(f"Wrong Answer. Have: '{output}'. Want: '{expected_output}'.")

        else:
            print("Correct!")
