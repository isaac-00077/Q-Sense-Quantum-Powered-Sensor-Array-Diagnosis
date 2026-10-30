<div align="center">

# ⚛️ Q-Sense
### Quantum Sensor Array Diagnosis with the Bernstein–Vazirani Algorithm

**Explore how quantum algorithms can identify a hidden sensor-pattern bitstring — through an interactive Streamlit simulation.**

[![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)](https://www.python.org/)
[![Qiskit](https://img.shields.io/badge/Quantum-Qiskit-6929C4)](https://www.ibm.com/quantum/qiskit)
[![Streamlit](https://img.shields.io/badge/UI-Streamlit-FF4B4B?logo=streamlit&logoColor=white)](https://streamlit.io/)
[![Simulation](https://img.shields.io/badge/Execution-Local%20Simulation-16803D)](https://qiskit.github.io/qiskit-aer/)

</div>

---

## 🌌 About the project

**Q-Sense** is an educational quantum-computing application that demonstrates the **Bernstein–Vazirani (BV) algorithm** using a sensor-array-inspired example.

The BV algorithm is designed to discover a hidden binary string by querying a specially constructed oracle. In this project, that hidden string is used as a model for a sensor pattern. The app introduces the theory, constructs a quantum circuit, simulates its execution locally, and displays the measurement results.

> **Important:** Q-Sense is a learning and simulation project. It does not connect to, monitor, or diagnose physical sensors.

## ✨ Highlights

- 📘 **Learn the theory** — explore the Bernstein–Vazirani algorithm and its core idea.
- 🧩 **Build a quantum circuit** — prepare input qubits, an ancilla qubit, gates, and measurements.
- 🖥️ **Run a local simulation** — use Qiskit Aer without needing a physical quantum computer.
- 🔍 **Inspect results** — compare the measured output with the configured hidden string.
- 📊 **Explore visualizations** — view circuit diagrams and result displays supported by the app.
- 🚨 **Demonstrate parity logic** — explore the project's simulated parity/alarm behaviour where implemented.

## 🧠 How it works

At a high level, the application follows this workflow:

1. **Choose a hidden bitstring** that represents the simulated sensor pattern.
2. **Construct the oracle circuit** that encodes the hidden string.
3. **Apply the Bernstein–Vazirani algorithm** using Hadamard gates and oracle operations.
4. **Transpile the circuit** so it is suitable for the selected simulator.
5. **Execute the circuit** with Qiskit Aer and measure the qubits.
6. **Inspect the output** and compare it with the expected hidden bitstring.

For an ideal Bernstein–Vazirani circuit, the input register reveals the hidden string in one algorithmic oracle query. Actual app output depends on the circuit implementation, measurement ordering, and simulator configuration.

## 🧰 Tech stack

| Technology | Role |
|---|---|
| [Python](https://www.python.org/) | Main programming language |
| [Qiskit](https://www.ibm.com/quantum/qiskit) | Quantum circuit creation and transpilation |
| [Qiskit Aer](https://qiskit.github.io/qiskit-aer/) | Local quantum-circuit simulation |
| [Streamlit](https://streamlit.io/) | Interactive web interface |
| [NumPy](https://numpy.org/) | Numerical operations, if used by the application |
| [Matplotlib](https://matplotlib.org/) | Plots and visualizations, if used by the application |
| [pylatexenc](https://github.com/phfaist/pylatexenc) | LaTeX-related rendering support where needed |

## 🚀 Get started

Follow these instructions to run the project on your computer after cloning the repository.

### Prerequisites

Install the following first:

- **Git** — to clone the repository
- **Python 3.10 or newer** — use a version supported by the installed Qiskit packages
- **pip** — Python package installer

Check your installations:

```bash
git --version
python --version
python -m pip --version
```

### 1. Clone the repository

Replace `<REPOSITORY-URL>` with this repository's Git URL:

```bash
git clone <REPOSITORY-URL>
```

### 2. Enter the project directory

```bash
cd <REPOSITORY-FOLDER>
```

Use the folder name created by Git when you cloned the repository.

### 3. Create a virtual environment

A virtual environment keeps this project's Python packages separate from other projects.

**Windows — Command Prompt:**

```bat
python -m venv .venv
.venv\Scripts\activate
```

**Windows — PowerShell:**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux:**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 4. Install dependencies

If `requirements.txt` is present in the repository root, run:

```bash
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If there is no dependency file, install the main packages directly:

```bash
python -m pip install streamlit qiskit qiskit-aer matplotlib numpy pylatexenc
```

### 5. Launch Q-Sense

If the Streamlit entry point is named `app.py`, start it with:

```bash
python -m streamlit run app.py
```

Streamlit will print a local address in the terminal, commonly:

**http://localhost:8501**

Open that address in your browser. Keep the terminal open while the app is running. If the main Python file has a different name, replace `app.py` with the correct filename.

## 🕹️ Using the application

1. Open the **Theory** section to review the algorithm and its example.
2. Navigate to the **Simulation** section.
3. Configure the hidden bitstring or oracle using the available controls.
4. Run the simulation.
5. Examine the circuit and measurement output.
6. Compare the recovered bitstring with the expected result.
7. Explore any parity or alarm indicators provided by the application.

The exact controls depend on the current implementation in the repository.

## 📁 Project structure

A typical layout may look like this:

```text
q-sense/
├── app.py                 # Streamlit application entry point
├── requirements.txt       # Python dependencies
└── README.md              # Project documentation
```

Your repository may contain additional modules, images, or assets. Keep those files in place because the application may depend on them.

## 🛠️ Troubleshooting

<details>
<summary><strong>Streamlit command not found</strong></summary>

Run Streamlit through Python:

```bash
python -m streamlit run app.py
```
</details>

<details>
<summary><strong>ModuleNotFoundError after installation</strong></summary>

Activate the virtual environment and install dependencies using the same Python interpreter:

```bash
python -m pip install -r requirements.txt
```

</details>

<details>
<summary><strong>Cannot find app.py</strong></summary>

Check that the terminal is in the repository root and confirm the actual name of the main Streamlit file.

</details>

<details>
<summary><strong>Qiskit Aer installation fails</strong></summary>

Check your Python version and read the full installation error. Use Python and package versions supported by the Qiskit and Qiskit Aer releases you are installing.

</details>

<details>
<summary><strong>The circuit diagram does not render</strong></summary>

Confirm that all declared dependencies are installed. Some drawing methods may require additional system or LaTeX support depending on how the circuit is rendered.

</details>

## 🔬 Concepts demonstrated

- Qubits and quantum gates
- Hadamard transformations
- Oracle-based computation
- The Bernstein–Vazirani algorithm
- Quantum-circuit transpilation
- Measurement and classical bitstrings
- Local quantum simulation

## 🤝 Contributing

Contributions and learning-focused improvements are welcome:

1. Fork the repository.
2. Create a branch for your changes.
3. Make and test your updates.
4. Commit your work with a descriptive message.
5. Open a pull request describing what changed.

## 🔐 Project hygiene

- Do not commit passwords, API keys, or other secrets.
- Avoid committing virtual environments such as `.venv/`.
- Keep dependencies documented in `requirements.txt`.
- Add a `LICENSE` file if you want to define how others may reuse the project.

## 📄 License

No license is specified by this README. Until a license is added, do not assume that the repository grants permission to redistribute or reuse the code.

---

<div align="center">

**Q-Sense** · Learning quantum algorithms, one circuit at a time ⚛️

</div>
