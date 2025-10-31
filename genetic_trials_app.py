import streamlit as st
import pandas as pd
import random

# -----------------------------
# Load Dataset
# -----------------------------
st.title("🧬 Genetic Algorithm Scheduling – Multiple Trials")

# Load the dataset (must be in the same folder or accessible via URL)
try:
    df = pd.read_csv("program_ratings_increased.csv")
    st.subheader("📄 Loaded Dataset: program_ratings_increased.csv")
    st.dataframe(df, use_container_width=True)
except FileNotFoundError:
    st.error("❌ CSV file 'program_ratings_increased.csv' not found. Please ensure it is in the same directory.")
    st.stop()

# -----------------------------
# Helper: Mock Genetic Algorithm Function
# -----------------------------
def run_genetic_algorithm(co_r, mut_r):
    """
    Simulated Genetic Algorithm that generates a random schedule.
    Replace this with your actual GA scheduling logic if available.
    """
    programs = df.sample(n=min(6, len(df)), random_state=int(co_r * 1000 + mut_r * 10000))["Program"].tolist() \
        if "Program" in df.columns else \
        ["Wildlife Documentary", "News", "Kids Show", "Sports Live", "Cooking Show", "Drama Series"]

    time_slots = ["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM"]

    # Shuffle to simulate GA optimization result
    random.seed(int(co_r * 1000 + mut_r * 10000))
    random.shuffle(programs)

    schedule = pd.DataFrame({
        "Time Slot": time_slots,
        "Program": programs
    })
    return schedule

# -----------------------------
# Sidebar Parameters
# -----------------------------
st.markdown("""
This interface lets you **experiment with three different parameter combinations**
for the Genetic Algorithm.  
Each trial will produce a separate optimized schedule.
""")

st.sidebar.header("⚙️ Genetic Algorithm Parameters")

# --- TRIAL 1 ---
st.sidebar.subheader("Trial 1 Parameters")
co_r1 = st.sidebar.slider("CO_R (Trial 1)", 0.0, 0.95, 0.8, 0.01)
mut_r1 = st.sidebar.slider("MUT_R (Trial 1)", 0.01, 0.05, 0.02, 0.01)

# --- TRIAL 2 ---
st.sidebar.subheader("Trial 2 Parameters")
co_r2 = st.sidebar.slider("CO_R (Trial 2)", 0.0, 0.95, 0.7, 0.01)
mut_r2 = st.sidebar.slider("MUT_R (Trial 2)", 0.01, 0.05, 0.03, 0.01)

# --- TRIAL 3 ---
st.sidebar.subheader("Trial 3 Parameters")
co_r3 = st.sidebar.slider("CO_R (Trial 3)", 0.0, 0.95, 0.9, 0.01)
mut_r3 = st.sidebar.slider("MUT_R (Trial 3)", 0.01, 0.05, 0.04, 0.01)

# -----------------------------
# Run Trials
# -----------------------------
if st.button("🚀 Run All Three Trials"):
    st.success("✅ Genetic Algorithm executed for all three trials!")

    # Store trial configurations
    trials = {
        "Trial 1": (co_r1, mut_r1),
        "Trial 2": (co_r2, mut_r2),
        "Trial 3": (co_r3, mut_r3)
    }

    # Run and display results
    for trial_name, (co_r, mut_r) in trials.items():
        st.subheader(f"📋 {trial_name}")
        st.write(f"**Crossover Rate (CO_R):** `{co_r}`")
        st.write(f"**Mutation Rate (MUT_R):** `{mut_r}`")

        # Run the (mock) GA
        schedule_df = run_genetic_algorithm(co_r, mut_r)

        # Display schedule
        st.dataframe(schedule_df, use_container_width=True)

        # Optional: Download schedule
        csv = schedule_df.to_csv(index=False).encode("utf-8")
        st.download_button(
            f"⬇️ Download {trial_name} Schedule as CSV",
            data=csv,
            file_name=f"{trial_name.lower().replace(' ', '_')}_schedule.csv",
            mime="text/csv"
        )

else:
    st.info("Set your parameters in the sidebar and click **Run All Three Trials** to generate schedules.")
