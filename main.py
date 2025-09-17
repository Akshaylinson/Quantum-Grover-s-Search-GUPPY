# main.py
"""
Grover's Search demo (2-3 qubits recommended)
Usage examples:
  python main.py --n 2 --marked 2 --shots 1024
  python main.py --n 3 --marked 5 --shots 2048
"""

import os
import math
import argparse
from collections import Counter

from qiskit.compiler import transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram
import matplotlib.pyplot as plt

from circuits.grover import build_grover_circuit


def recommend_iterations(n: int) -> int:
    """Return recommended number of Grover iterations: floor(pi/4 * sqrt(N))."""
    N = 2 ** n
    return max(1, int(math.floor((math.pi / 4) * math.sqrt(N))))


def run_grover(n: int, marked: int, shots: int, iterations: int = None, out_folder: str = "results"):
    if iterations is None:
        iterations = recommend_iterations(n)

    print(f"Grover: n={n}, N={2**n}, marked={marked}, iterations={iterations}, shots={shots}")

    qc = build_grover_circuit(n, marked, iterations)
    print("\nCircuit (text):\n")
    print(qc.draw(output="text"))

    backend = AerSimulator()
    compiled = transpile(qc, backend)
    job = backend.run(compiled, shots=shots)
    result = job.result()
    counts = result.get_counts()

    # Print and save results
    print("\nRaw counts:")
    print(counts)

    os.makedirs(out_folder, exist_ok=True)
    out_txt = os.path.join(out_folder, "grover_results.txt")
    with open(out_txt, "w") as f:
        f.write(f"n={n}, N={2**n}, marked={marked}, iterations={iterations}, shots={shots}\n\n")
        f.write("Circuit (text):\n")
        f.write(qc.draw(output="text") + "\n\n")
        f.write("Counts:\n")
        for k, v in sorted(counts.items(), key=lambda kv: kv[1], reverse=True):
            f.write(f"{k} : {v}\n")
    print(f"\nSaved results to: {out_txt}")

    # Plot histogram and save
    fig = plt.figure(figsize=(6, 4))
    plot_histogram(counts)
    plt.title(f"Grover results (n={n}, marked={marked}, iter={iterations})")
    hist_path = os.path.join(out_folder, "grover_hist.png")
    plt.tight_layout()
    fig.savefig(hist_path)
    print(f"Saved histogram to: {hist_path}")

    plt.show()
    return counts


def parse_args():
    p = argparse.ArgumentParser(description="Grover's search demo")
    p.add_argument("--n", type=int, choices=[1, 2, 3], default=2, help="Number of qubits (1-3)")
    p.add_argument("--marked", type=int, default=1, help="Index of marked element (0..2^n - 1)")
    p.add_argument("--shots", type=int, default=1024, help="Shots / samples")
    p.add_argument("--iterations", type=int, default=None, help="Number of Grover iterations (overrides recommendation)")
    p.add_argument("--out", type=str, default="results", help="Output folder")
    return p.parse_args()


if __name__ == "__main__":
    args = parse_args()
    N = 2 ** args.n
    if args.marked < 0 or args.marked >= N:
        raise SystemExit(f"Marked must be in [0, {N-1}] for n={args.n}")
    run_grover(n=args.n, marked=args.marked, shots=args.shots, iterations=args.iterations, out_folder=args.out)

