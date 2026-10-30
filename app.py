import streamlit as st
from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator

# ============================================================
# Bernstein–Vazirani: Five-Sensor Hidden Subset Demonstration
# ============================================================

N_SENSORS = 5
ANCILLA = 5
TOTAL_QUBITS = 6
DEFAULT_SECRET = "11000"
DEFAULT_INPUT = "00000"
DEFAULT_TEST_INPUT = "00000"


st.set_page_config(
    page_title="Sensor Array Diagnosis | Bernstein–Vazirani",
    page_icon="⚛️",
    layout="wide",
)

st.title("⚛️ Sensor Array Diagnosis")
st.caption(
    "Bernstein–Vazirani algorithm • Five sensor qubits + one ancilla qubit"
)


def valid_bitstring(value: str, length: int = 5) -> bool:
    return len(value) == length and all(bit in "01" for bit in value)


def xor_bits(left: str, right: str) -> str:
    """Return bitwise XOR for two equal-length binary strings."""
    return "".join(str(int(a) ^ int(b)) for a, b in zip(left, right))


def selected_sensors(secret: str) -> list[int]:
    """Return 1-based sensor numbers whose secret bit is 1."""
    return [i + 1 for i, bit in enumerate(secret) if bit == "1"]


def parity_function(secret: str, sensor_input: str) -> int:
    """f_s(x) = s dot x mod 2."""
    return sum(int(a) * int(b) for a, b in zip(secret, sensor_input)) % 2


def build_bv_circuit(secret: str, initial_input: str) -> QuantumCircuit:
    """
    Build the six-qubit circuit.

    q0-q4: five sensor/input qubits
    q5: ancilla qubit

    Qiskit initializes all qubits to |0...0>.
    X gates on q0-q4 prepare the requested initial basis input.
    X then H on q5 prepares the ancilla in |->.
    Oracle CNOTs encode each 1 in the secret.
    Final H gates decode the secret XOR initial input.
    """
    qc = QuantumCircuit(TOTAL_QUBITS, N_SENSORS)

    # Prepare the requested five-bit initial basis state.
    # The leftmost string bit maps to q0, matching the app's sensor labels.
    for i, bit in enumerate(initial_input):
        if bit == "1":
            qc.x(i)

    # Prepare ancilla |0> -> |1> -> |->
    qc.x(ANCILLA)
    qc.h(ANCILLA)

    # Create superposition on the five sensor qubits.
    for i in range(N_SENSORS):
        qc.h(i)

    qc.barrier(label="Oracle")

    # Oracle for f_s(x) = s dot x mod 2.
    # A CNOT is placed for each secret bit equal to 1.
    for i, bit in enumerate(secret):
        if bit == "1":
            qc.cx(i, ANCILLA)

    qc.barrier(label="Decode")

    # Decode the hidden string.
    for i in range(N_SENSORS):
        qc.h(i)

    # Measure only the five sensor qubits; ancilla is not measured.
    for i in range(N_SENSORS):
        qc.measure(i, i)

    return qc


def run_simulation(qc: QuantumCircuit, shots: int = 1024):
    simulator = AerSimulator()
    compiled = transpile(qc, simulator)
    result = simulator.run(compiled, shots=shots).result()
    raw_counts = result.get_counts()

    # Qiskit prints classical bit strings in reverse register order.
    # Reverse to display in the same left-to-right order as the app inputs.
    counts = {bits[::-1]: count for bits, count in raw_counts.items()}
    most_frequent = max(counts, key=counts.get)
    return counts, most_frequent


theory_tab, simulation_tab = st.tabs(["📘 Theory & equations", "🧪 Simulation"])

with theory_tab:
    st.header("Bernstein–Vazirani algorithm: theory")
    st.write(
        "The objective is to identify a hidden five-bit string "
        r"$s=s_0s_1s_2s_3s_4$ using the oracle for the parity function."
    )

    st.subheader("Core formulas")
    st.markdown("**Hidden parity function**")
    st.latex(r"f_s(x)=s\cdot x \bmod 2=\bigoplus_{i=0}^{4}(s_i\land x_i)")
    st.markdown("**Quantum oracle**")
    st.latex(r"U_f\lvert x,y\rangle=\lvert x,\,y\oplus f_s(x)\rangle")
    st.markdown("**Ancilla prepared for phase kickback**")
    st.latex(r"\lvert 0\rangle\xrightarrow{X}\lvert 1\rangle"
             r"\xrightarrow{H}\lvert-\rangle=\frac{\lvert0\rangle-\lvert1\rangle}{\sqrt2}")
    st.markdown("**Effect of the oracle with the ancilla in $\\lvert-\\rangle$**")
    st.latex(r"U_f\big(\lvert x\rangle\lvert-\rangle\big)"
             r"=(-1)^{f_s(x)}\lvert x\rangle\lvert-\rangle")
    st.markdown("**Final decoding and optional nonzero initial input**")
    st.latex(r"\lvert a\rangle\xrightarrow{H^{\otimes5},\,U_f,\,H^{\otimes5}}"
             r"\lvert a\oplus s\rangle")
    st.latex(r"m=a\oplus s\qquad\Longrightarrow\qquad s=a\oplus m")
    st.info(
        "For standard BV, use initial input a = 00000. Then the measured result m is "
        "the secret s directly. If a is nonzero, the measured result is a XOR s, "
        "so a second classical XOR recovers s."
    )

    st.subheader("What each stage does")
    st.markdown(
        """
1. **Initialize:** all six qubits begin in `|000000⟩`. The first five are sensor/input
   qubits `q0`–`q4`; `q5` is the ancilla.
2. **Prepare the initial input:** an X gate is placed on each sensor qubit whose
   chosen initial-input bit is `1`. Thus `00000` needs no X gates, while `10000`
   needs an X on `q0`.
3. **Prepare the ancilla:** X changes `q5` from `|0⟩` to `|1⟩`; H changes it to
   `|−⟩ = (|0⟩ − |1⟩)/√2`.
4. **First Hadamards:** H is applied to all five sensor qubits, creating superposition.
   Each basis component gets a phase determined by the initial input `a`.
5. **Oracle CNOTs:** for every `1` in secret `s`, add a CNOT from the corresponding
   sensor qubit to ancilla `q5`. With `s = 11000`, the controls are `q0` and `q1`.
   Because `q5` is in `|−⟩`, each controlled flip contributes a phase of −1 when
   its control is 1. Together these phases encode the parity function.
6. **Second Hadamards (decode):** H is applied again to `q0`–`q4`. The phases interfere
   so the sensor register becomes the basis state `|a XOR s⟩`.
7. **Measurement:** measure `q0`–`q4`. The ancilla is not measured because it is not
   the five-bit answer.
"""
    )

    st.subheader("Worked example A — initial input `00000`")
    example_secret = "11000"
    st.markdown("Use hidden secret **`s = 11000`**, so the oracle contains CNOTs from `q0` and `q1` to `q5`.")
    with st.container(border=True):
        st.markdown("**Step 1 — Initialize and prepare input**")
        st.latex(r"\lvert a\rangle=\lvert00000\rangle")
        st.write("No X gates are added to q0–q4, because every initial-input bit is 0.")
        st.markdown("**Step 2 — Prepare ancilla**")
        st.latex(r"q_5:\ \lvert0\rangle\xrightarrow{X}\lvert1\rangle"
                 r"\xrightarrow{H}\lvert-\rangle")
        st.markdown("**Step 3 — Apply the first H gates**")
        st.latex(r"\lvert00000\rangle\xrightarrow{H^{\otimes5}}\lvert+\rangle^{\otimes5}"
                 r"=\frac{1}{\sqrt{32}}\sum_{x\in\{0,1\}^5}\lvert x\rangle")
        st.write("All 32 five-bit basis states are in superposition; the ancilla remains |−⟩.")
        st.markdown("**Step 4 — Oracle CNOTs for `11000`**")
        st.write("CNOT(q0, q5) and CNOT(q1, q5) implement the secret. Phase kickback gives:")
        st.latex(r"\frac{1}{\sqrt{32}}\sum_x(-1)^{x_0\oplus x_1}\lvert x\rangle"
                 r"\lvert-\rangle")
        st.write("The phase is negative exactly when x₀ XOR x₁ = 1. The computational-basis labels are not measured yet.")
        st.markdown("**Step 5 — Apply the second H gates**")
        st.latex(r"H^{\otimes5}\left(\frac{1}{\sqrt{32}}\sum_x"
                 r"(-1)^{x_0\oplus x_1}\lvert x\rangle\right)=\lvert11000\rangle")
        st.markdown("**Step 6 — Measure**")
        st.success("Measured output: `11000` — this directly equals the hidden secret.")

    st.subheader("Worked example B — initial input `10000`")
    st.markdown("Keep the same hidden secret **`s = 11000`**, but choose initial input **`a = 10000`**.")
    with st.container(border=True):
        st.markdown("**Step 1 — Initialize and prepare input**")
        st.latex(r"\lvert00000\rangle\xrightarrow{X\text{ on }q_0}\lvert10000\rangle")
        st.write("The X gate is applied to the default zero on q0, preparing a one. It does not cancel a previously prepared one.")
        st.markdown("**Step 2 — Prepare ancilla**")
        st.latex(r"q_5:\ \lvert0\rangle\xrightarrow{X}\lvert1\rangle"
                 r"\xrightarrow{H}\lvert-\rangle")
        st.markdown("**Step 3 — Apply the first H gates**")
        st.latex(r"\lvert10000\rangle\xrightarrow{H^{\otimes5}}"
                 r"\frac{1}{\sqrt{32}}\sum_x(-1)^{x_0}\lvert x\rangle")
        st.write("The initial `1` on q0 makes the terms with x₀ = 1 have a negative phase.")
        st.markdown("**Step 4 — Oracle CNOTs for `11000`**")
        st.write("CNOT(q0, q5) and CNOT(q1, q5) encode the secret parity. The phases combine:")
        st.latex(r"\frac{1}{\sqrt{32}}\sum_x(-1)^{x_0}"
                 r"(-1)^{x_0\oplus x_1}\lvert x\rangle\lvert-\rangle"
                 r"=\frac{1}{\sqrt{32}}\sum_x(-1)^{x_1}\lvert x\rangle\lvert-\rangle")
        st.write("The phase factors combine by XOR: x₀ XOR (x₀ XOR x₁) = x₁.")
        st.markdown("**Step 5 — Apply the second H gates**")
        st.latex(r"H^{\otimes5}\left(\frac{1}{\sqrt{32}}\sum_x"
                 r"(-1)^{x_1}\lvert x\rangle\right)=\lvert01000\rangle")
        st.markdown("**Step 6 — Measure, then recover the secret classically**")
        st.warning("Measured output: `01000`. This is not the secret by itself because the initial input was nonzero.")
        st.latex(r"m=a\oplus s=10000\oplus11000=01000")
        st.latex(r"s=a\oplus m=10000\oplus01000=11000")
        st.success("Recovered secret after XOR: `11000`.")

    st.subheader("Why the H gates matter")
    st.markdown(
        """
- The **first H layer** creates superposition so the oracle's parity information can
  affect relative phases across the sensor-register basis states.
- The **oracle CNOTs** encode the secret through phase kickback using the ancilla in
  `|−⟩`.
- The **second H layer** converts those relative phases into a deterministic
  computational-basis bit string.
- With initial input `00000`, the final string is the secret. With initial input
  `10000`, this version of the circuit returns `01000`, and `10000 XOR 01000`
  recovers `11000`.
"""
    )

    st.subheader("Sensor alarm parity is a separate demonstration")
    st.latex(r"f_s(x_{\mathrm{test}})=s\cdot x_{\mathrm{test}}\bmod2")
    st.write(
        "The sensor test input is used separately to demonstrate whether the selected "
        "sensors have odd or even parity. It is not the BV initial input and does not "
        "change the quantum measurement."
    )


with simulation_tab:
    st.header("Simulation configuration")

    with st.expander("Oracle configuration", expanded=True):
        secret = st.text_input(
            "Hidden sensor pattern (5 bits)",
            value=DEFAULT_SECRET,
            max_chars=N_SENSORS,
            help="The 1-bits determine which sensor qubits control CNOT gates in the oracle.",
            key="oracle_secret",
        ).strip()
        if not valid_bitstring(secret):
            st.error("Enter exactly five binary digits (0 or 1), e.g. 11000.")
            st.stop()
        st.success(f"Configured secret: `{secret}`")
        sensors = selected_sensors(secret)
        if sensors:
            st.write("Selected sensors: " + ", ".join(map(str, sensors)))
        else:
            st.write("Selected sensors: none (secret is `00000`)")

    col1, col2 = st.columns(2)
    with col1:
        initial_input = st.text_input(
            "BV initial input (5 bits)",
            value=DEFAULT_INPUT,
            max_chars=N_SENSORS,
            help="Use 00000 for standard BV secret recovery. Other inputs are supported.",
            key="bv_initial_input",
        ).strip()
    with col2:
        sensor_test_input = st.text_input(
            "Sensor test input (5 bits)",
            value=DEFAULT_TEST_INPUT,
            max_chars=N_SENSORS,
            help="Optional parity/alarm demonstration. This input is separate from the BV initial input.",
            key="sensor_test_input",
        ).strip()

    if not valid_bitstring(initial_input):
        st.error("BV initial input must contain exactly five binary digits.")
        st.stop()
    if not valid_bitstring(sensor_test_input):
        st.error("Sensor test input must contain exactly five binary digits.")
        st.stop()

    st.subheader("Oracle CNOT placement")
    if sensors:
        st.write("CNOT gates: " + ", ".join(f"Sensor {n}" for n in sensors))
    else:
        st.write("CNOT gates: none")

    st.caption(
        "The circuit below updates when you change the secret or initial input. "
        "The quantum simulation runs only when you click the button."
    )

    circuit = build_bv_circuit(secret, initial_input)

    # Display the circuit diagram, but do not display a measurement histogram/chart.
    try:
        circuit_image = circuit.draw(output="mpl", fold=-1, style="clifford")
        st.pyplot(circuit_image, clear_figure=True)
    except Exception as exc:
        st.warning(
            "The circuit image could not be rendered. Install the optional drawing "
            "dependency with `python -m pip install pylatexenc`, then restart Streamlit."
        )
        with st.expander("Show circuit as text instead"):
            st.code(circuit.draw(output="text").__str__())
        st.caption(f"Drawing detail: {exc}")

    parity = parity_function(secret, sensor_test_input)
    st.subheader("Optional sensor parity test")
    pcol1, pcol2 = st.columns(2)
    with pcol1:
        st.metric("Parity result", str(parity))
    with pcol2:
        st.metric("Alarm status", "🔔 ALARM" if parity == 1 else "✅ No alarm")
    st.caption(
        "The parity/alarm test is a separate classical evaluation of the same function. "
        "It does not change the BV circuit measurement."
    )

    if st.button("▶ Run simulation", type="primary"):
        with st.spinner("Running the quantum simulator..."):
            counts, most_frequent = run_simulation(circuit, shots=1024)

        expected_measured = xor_bits(initial_input, secret)
        recovered_secret = xor_bits(initial_input, most_frequent)
        correct_shots = counts.get(expected_measured, 0)

        st.subheader("Simulation results")
        result_col1, result_col2 = st.columns(2)
        with result_col1:
            st.metric("Most frequent measured output", most_frequent)
        with result_col2:
            st.metric("Expected measured output", expected_measured)

        st.metric("Correct shots", f"{correct_shots} / 1024")

        if initial_input == "00000":
            st.success(
                f"Recovered hidden secret: {most_frequent}. "
                "Because the initial input is 00000, the measured output is the secret directly."
            )
        else:
            st.info(
                f"Measured output: {most_frequent}\n\n"
                f"Recovery: {initial_input} XOR {most_frequent} = {recovered_secret}"
            )
            if recovered_secret == secret:
                st.success(f"Recovered hidden secret: {recovered_secret}")
            else:
                st.error(
                    "The recovered value does not match the configured secret. "
                    "Check bit ordering and the circuit implementation."
                )

        st.caption(
            "No histogram/chart is shown. In an ideal simulator, the expected result "
            "should appear in every shot."
        )

st.divider()
st.caption(
    "Educational simulator. Real quantum hardware may produce different results "
    "because of noise and measurement errors."
)
