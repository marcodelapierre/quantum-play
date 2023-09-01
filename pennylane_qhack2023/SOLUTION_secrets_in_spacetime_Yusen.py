import json
import pennylane as qml
import pennylane.numpy as np

def U_psi(theta):
    """
    Quantum function that generates |psi>, Zenda's state wants to send to Reece.

    Args:
        theta (float): Parameter that generates the state.

    """
    qml.Hadamard(wires = 0)
    qml.CRX(theta, wires = [0,1])
    qml.CRZ(theta, wires = [0,1])

def is_unsafe(alpha, beta, epsilon):
    """
    Boolean function that we will use to know if a set of parameters is unsafe.

    Args:
        alpha (float): parameter used to encode the state.
        beta (float): parameter used to encode the state.
        epsilon (float): unsafe-tolerance.

    Returns:
        (bool): 'True' if alpha and beta are epsilon-unsafe coefficients. 'False' in the other case.

    """


    dev = qml.device("default.qubit", wires=2)
    @qml.qnode(dev)
    def loss(theta, alpha, beta):
        qml.Hadamard(wires = 0)
        qml.CRX(theta, wires = [0,1])
        qml.CRZ(theta, wires = [0,1])
        
        qml.RZ(alpha, wires = 0)
        qml.RZ(alpha, wires = 1)
        
        qml.RX(beta, wires = 0)
        qml.RX(beta, wires = 1)
        
        qml.adjoint(qml.CRZ(theta, wires = [0,1]))
        qml.adjoint(qml.CRX(theta, wires = [0,1]))
        qml.adjoint(qml.Hadamard(wires = 0))
        
        prob = qml.probs(wires = [0, 1])
        #print(prob)
        return prob
    
    optimizer = qml.GradientDescentOptimizer()
    steps = 1000
    theta = np.array([0])
    for i in range(steps):
        theta = optimizer.step(lambda theta: (-loss(theta, alpha, beta)[0]), theta)
    # Put your code here #
    # model(params)
    result = loss(theta, alpha, beta)[0]
    if (result >= 1 - epsilon):
        return True
    else:
        return False


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    output = is_unsafe(*ins)
    return str(output)

def check(solution_output: str, expected_output: str) -> None:
    
    def bool_to_int(string):
        if string == "True":
            return 1
        return 0

    solution_output = bool_to_int(solution_output)
    expected_output = bool_to_int(expected_output)
    assert solution_output == expected_output, "The solution is not correct."

test_cases = [['[0.1, 0.2, 0.3]', 'True'], ['[1.1, 1.2, 0.3]', 'False'], ['[1.1, 1.2, 0.4]', 'True'], ['[0.5, 1.9, 0.7]', 'True']]

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
