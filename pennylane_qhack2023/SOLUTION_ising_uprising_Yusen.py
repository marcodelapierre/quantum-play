import json
import pennylane as qml
import pennylane.numpy as np

def create_Hamiltonian(h):
    """
    Function in charge of generating the Hamiltonian of the statement.

    Args:
        h (float): magnetic field strength

    Returns:
        (qml.Hamiltonian): Hamiltonian of the statement associated to h
    """


    H_ising = qml.Hamiltonian(
        [-1, -1, -1 , -1, -h, -h, -h, -h],
        [qml.PauliZ(0) @ qml.PauliZ(1), qml.PauliZ(1) @ qml.PauliZ(2), qml.PauliZ(2) @ qml.PauliZ(3), qml.PauliZ(3) @ qml.PauliZ(0), qml.PauliX(0), qml.PauliX(1), qml.PauliX(2), qml.PauliX(3)]
    )
    return H_ising


dev = qml.device("default.qubit", wires=4)

@qml.qnode(dev)
def model(params, H):
    """
    To implement VQE you need an ansatz for the candidate ground state!
    Define here the VQE ansatz in terms of some parameters (params) that
    create the candidate ground state. These parameters will
    be optimized later.

    Args:
        params (numpy.array): parameters to be used in the variational circuit
        H (qml.Hamiltonian): Hamiltonian used to calculate the expected value

    Returns:
        (float): Expected value with respect to the Hamiltonian H
    """


     #H = create_Hamiltonian(1)
  
    H_ancc = qml.Hamiltonian(
        [-1, -1, -1, -1],
        [qml.PauliX(0), qml.PauliX(1), qml.PauliX(2), qml.PauliX(3)]
    )
    wires = range(4)
    
    for w in wires:
        qml.Hadamard(wires=w)

    qml.ApproxTimeEvolution(H, params[0], 10)
    qml.ApproxTimeEvolution(H_ancc, params[1], 10)
    
    qml.ApproxTimeEvolution(H, params[2], 10)
    qml.ApproxTimeEvolution(H_ancc, params[3], 10)
    
    qml.ApproxTimeEvolution(H, params[4], 10)
    qml.ApproxTimeEvolution(H_ancc, params[5], 10)
    
    qml.ApproxTimeEvolution(H, params[6], 10)
    qml.ApproxTimeEvolution(H_ancc, params[7], 10)
    return qml.expval(H)


def train(h):
    """
    In this function you must design a subroutine that returns the
    parameters that best approximate the ground state.

    Args:
        h (float): magnetic field strength

    Returns:
        (numpy.array): parameters that best approximate the ground state.
    """



    H = create_Hamiltonian(h)
    #from scipy.optimize import minimize
    optimizer = qml.GradientDescentOptimizer()
    steps = 50
    params = np.array([0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5, 0.5])
    for i in range(steps):
        params = optimizer.step(lambda params: model(params, H), params)
    #minimize(lambda alpha: Loss_function(alpha, train_data, labels), alpha)
    #print("Optimal Parameters")
    #print(params)
    #print(model(params, H))
    
    return (params)


# These functions are responsible for testing the solution.
def run(test_case_input: str) -> str:
    ins = json.loads(test_case_input)
    params = train(ins)
    return str(model(params, create_Hamiltonian(ins)))


def check(solution_output: str, expected_output: str) -> None:
    solution_output = json.loads(solution_output)
    expected_output = json.loads(expected_output)
    assert np.allclose(
        solution_output, expected_output, rtol=1e-1
    ), "The expected value is not correct."

test_cases = [['1.0', '-5.226251859505506'], ['2.3', '-9.66382463698038']]

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
