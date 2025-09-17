 🔍 Quantum Grover’s Search (Qiskit Implementation)

A practical demonstration of **Grover’s Search Algorithm** using [Qiskit](https://qiskit.org/).  
Grover’s algorithm is one of the most famous quantum algorithms, designed to search through an **unsorted database** exponentially faster than classical methods.  

Instead of **N** steps (classical), Grover’s finds the target in roughly **√N steps** using amplitude amplification.  
This project showcases Grover’s algorithm on **2–3 qubits**, highlighting how the correct solution "stands out" in measurement results.  

---

## ✨ Features
- Implementation of Grover’s Algorithm for 2–3 qubits.
- Oracle + Diffuser construction for marked state search.
- Runs on **Qiskit Aer Simulator**.
- Saves results to `results/grover_results.txt`.
- Visualizes probability distribution with `matplotlib`.

---

## 📂 Project Structure
quantum-grover-guppy/
│── main.py # Entry point – runs Grover’s search
│── circuits/
│ └── grover.py # Defines oracle & Grover circuit
│── results/
│ └── grover_results.txt # Output results
│── requirements.txt # Dependencies
│── README.md # Project documentation

yaml
Copy code

---

## ⚡ Installation
1. Create & activate a virtual environment:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate   # On Windows
   source .venv/bin/activate # On Mac/Linux
Install dependencies:

bash
Copy code
pip install -r requirements.txt
▶️ Usage
Run the Grover search:

bash
Copy code
python main.py
Expected output:

Prints the most likely solution to console.

Saves result counts to results/grover_results.txt.

Displays a histogram of measurement probabilities.

📊 Example Output
yaml
Copy code
Most probable solution: |11⟩
And the histogram will show a clear spike at the correct state.

🔮 What You’ll Learn
How quantum oracles work.

The role of amplitude amplification (diffuser).

Why Grover’s search provides a quadratic speedup.

📖 References
Qiskit Textbook – Grover’s Algorithm

IBM Quantum

