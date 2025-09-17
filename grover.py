# circuits/grover.py
"""
Grover's algorithm circuits for n-qubit search (n = 2 or 3 recommended).
Provides:
 - build_oracle(n, marked_index)
 - build_diffuser(n)
 - build_grover_circuit(n, marked_index, iterations)
"""

from qiskit import QuantumCircuit


def index_to_bitstring(index: int, n: int) -> str:
    """Return an n-bit binary string (MSB left) for index."""
    return format(index, f"0{n}b")


def build_oracle(n: int, marked_index: int) -> QuantumCircuit:
    """
    Build an oracle that flips the sign of the |marked_index> basis state.
    Implementation approach (phase oracle):
      - For each bit of marked bitstring that equals '0', apply an X gate.
      - Then apply multi-controlled Z (via H on target + multi-controlled X) to flip phase.
      - Undo the X gates.
    Qiskit note: For small n we can implement a controlled-Z using `mcx` + H trick.
    """
    if marked_index < 0 or marked_index >= 2**n:
        raise ValueError("marked_index out of range")

    bs = index_to_bitstring(marked_index, n)
    qc = QuantumCircuit(n, name=f"Oracle({bs})")

    # Flip qubits where bit is '0' so that the marked state maps to |11...1>
    for i, b in enumerate(bs):
        if b == "0":
            qc.x(i)

    # Implement multi-controlled Z:
    # For n>=2, controlled-Z with all controls -> apply H to last qubit,
    # then multi-controlled X (mcx) with last qubit as target, then H back.
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        # Use mcx with controls qubits [0..n-2] and target n-1
        controls = list(range(0, n - 1))
        qc.mcx(controls, n - 1)
        qc.h(n - 1)

    # Undo the initial Xs
    for i, b in enumerate(bs):
        if b == "0":
            qc.x(i)

    return qc


def build_diffuser(n: int) -> QuantumCircuit:
    """
    Build the diffuser (inversion about the mean) for n qubits:
    - H on all qubits
    - X on all qubits
    - multi-controlled Z (same trick)
    - X on all qubits
    - H on all qubits
    """
    qc = QuantumCircuit(n, name="Diffuser")

    # H and X on all
    qc.h(range(n))
    qc.x(range(n))

    # multi-controlled Z
    if n == 1:
        qc.z(0)
    else:
        qc.h(n - 1)
        controls = list(range(0, n - 1))
        qc.mcx(controls, n - 1)
        qc.h(n - 1)

    # undo X and H
    qc.x(range(n))
    qc.h(range(n))
    return qc


def build_grover_circuit(n: int, marked_index: int, iterations: int) -> QuantumCircuit:
    """
    Build full Grover circuit:
      - Initialize in uniform superposition
      - Repeat (oracle + diffuser) `iterations` times
      - Measure all qubits
    """
    if n < 1:
        raise ValueError("n must be >= 1")

    qc = QuantumCircuit(n, n)
    # Initialize |s> = H on all qubits
    qc.h(range(n))

    oracle = build_oracle(n, marked_index)
    diffuser = build_diffuser(n)

    for _ in range(iterations):
        qc.append(oracle.to_instruction(), range(n))
        qc.append(diffuser.to_instruction(), range(n))

    # Measure all to classical bits
    qc.measure(range(n), range(n))

    return qc

