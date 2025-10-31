import streamlit as st

# --- App Title ---
st.title("Genetic Algorithm Parameter Configuration")

st.markdown("""
This interface allows you to set the parameters for the Genetic Algorithm (GA).
Adjust the **Crossover Rate (CO_R)** and **Mutation Rate (MUT_R)** interactively.
""")

# --- Parameter Inputs ---
st.subheader("🔧 Parameter Settings")

# Crossover Rate input
co_r = st.slider(
    "Crossover Rate (CO_R)",
    min_value=0.0,
    max_value=0.95,
    value=0.8,
    step=0.01,
    help="Controls how much of the genetic material is exchanged between parents."
)

# Mutation Rate input
mut_r = st.slider(
    "Mutation Rate (MUT_R)",
    min_value=0.01,
    max_value=0.05,
    value=0.02,
    step=0.01,
    help="Controls the frequency of random mutations in the population."
)

# --- Display chosen parameters ---
st.subheader("📊 Selected Parameters")
st.write(f"**Crossover Rate (CO_R):** {co_r}")
st.write(f"**Mutation Rate (MUT_R):** {mut_r}")

# --- Optional: Button to confirm ---
if st.button("Confirm Parameters"):
    st.success(f"Parameters confirmed:\n- CO_R = {co_r}\n- MUT_R = {mut_r}")

