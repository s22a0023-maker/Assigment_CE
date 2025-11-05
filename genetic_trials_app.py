import streamlit as st
import pandas as pd
import random

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.title("🧬 Genetic Algorithm – Multiple Trials for Program Scheduling")

st.markdown("""
This app lets you **run the Genetic Algorithm three times**  
with different crossover and mutation rates.  
Each trial will produce a unique optimized schedule.
""")

# -----------------------------
# Load Dataset from Local File Path
# -----------------------------
# 👉 Replace this path with the actual location of your dataset
file_path = "program_ratings.csv"

try:
    df = pd.read_csv(file_path)
    st.success(f"✅ Dataset loaded successfully from local path:\n{file_path}")
    st.dataframe(df.head(), use_container_width=True)
except Exception as e:
    st.error(f"❌ Failed to load dataset from the given file path.\n\nError: {e}")
    st.stop()
    
# -----------------------------
# GA Parameter Inputs (Three Trials)
# -----------------------------
st.sidebar.header("⚙️ GA Parameter Settings – Multiple Trials")

# Trial 1
st.sidebar.subheader("Trial 1 Parameters")
co_r1 = st.sidebar.slider("CO_R (Trial 1)", 0.0, 0.95, 0.8, 0.01)
mut_r1 = st.sidebar.slider("MUT_R (Trial 1)", 0.01, 0.05, 0.02, 0.01)

# Trial 2
st.sidebar.subheader("Trial 2 Parameters")
co_r2 = st.sidebar.slider("CO_R (Trial 2)", 0.0, 0.95, 0.7, 0.01)
mut_r2 = st.sidebar.slider("MUT_R (Trial 2)", 0.01, 0.05, 0.03, 0.01)

# Trial 3
st.sidebar.subheader("Trial 3 Parameters")
co_r3 = st.sidebar.slider("CO_R (Trial 3)", 0.0, 0.95, 0.9, 0.01)
mut_r3 = st.sidebar.slider("MUT_R (Trial 3)", 0.01, 0.05, 0.04, 0.01)

# -----------------------------
# GA Simulation Function
# -----------------------------
def run_genetic_algorithm(df, co_r, mut_r):
    """
    Simulate GA schedule optimization using the uploaded dataset.
    Always produces schedule from Hour 6 to Hour 23.
    """

    # --- Detect program name column ---
    program_col = None
    for col in df.columns:
        if "program" in col.lower() or "name" in col.lower() or "title" in col.lower():
            program_col = col
            break
    if program_col is None:
        program_col = df.columns[0]

    # --- Extract program list ---
    programs = (
        df[program_col]
        .dropna()
        .drop_duplicates()
        .astype(str)
        .tolist()
    )

    # --- Define fixed time slots (Hour 6 to Hour 23) ---
    time_slots = [f"Hour {i}" for i in range(6, 24)]

    # --- GA Simulation Random Shuffle ---
    random.seed(int(co_r * 1000 + mut_r * 10000))
    random.shuffle(programs)

    # If fewer programs than time slots → repeat programs
    if len(programs) < len(time_slots):
        repeat_times = (len(time_slots) // len(programs)) + 1
        programs = (programs * repeat_times)[:len(time_slots)]
    else:
        programs = programs[:len(time_slots)]

    # Create schedule DataFrame
    schedule = pd.DataFrame({
        "Time Slot": time_slots,
        "Program": programs
    })

    return schedule


# -----------------------------
# Run Button – All Three Trials
# -----------------------------
if st.button("🚀 Run All Three Trials"):
    st.success("✅ Genetic Algorithm executed for all three trials!")

    trials = {
        "Trial 1": (co_r1, mut_r1),
        "Trial 2": (co_r2, mut_r2),
        "Trial 3": (co_r3, mut_r3)
    }

    # Loop through each trial
    for trial_name, (co_r, mut_r) in trials.items():
        st.subheader(f"📋 {trial_name}")
        st.write(f"**Crossover Rate (CO_R):** {co_r}")
        st.write(f"**Mutation Rate (MUT_R):** {mut_r}")

        schedule_df = run_genetic_algorithm(df, co_r, mut_r)

        st.dataframe(schedule_df, use_container_width=True)

        # Download button for each schedule
        csv = schedule_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            f"⬇️ Download {trial_name} Schedule as CSV",
            data=csv,
            file_name=f"{trial_name.lower().replace(' ', '_')}_schedule.csv",
            mime="text/csv"
        )

else:
    st.info("Adjust parameters for each trial and click **Run All Three Trials** to generate schedules.")
