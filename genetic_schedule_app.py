import streamlit as st
import pandas as pd
import random

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.title("Genetic Algorithm – Program Scheduling")

st.markdown("""
This app allows you to configure the **Genetic Algorithm parameters** and view the resulting **optimized schedule**.
""")

# --- Parameter Inputs ---
st.sidebar.header("⚙️ GA Parameter Settings")

co_r = st.sidebar.slider(
    "Crossover Rate (CO_R)",
    min_value=0.0,
    max_value=0.95,
    value=0.8,
    step=0.01,
    help="Controls how much of the genetic material is exchanged between parents."
)

mut_r = st.sidebar.slider(
    "Mutation Rate (MUT_R)",
    min_value=0.01,
    max_value=0.05,
    value=0.02,
    step=0.01,
    help="Controls the frequency of random mutations in the population."
)

st.sidebar.markdown(f"**Selected Parameters:**\n\n- CO_R: `{co_r}`\n- MUT_R: `{mut_r}`")

# -----------------------------
# Simulate a Genetic Algorithm (Mock Example)
# -----------------------------
def run_genetic_algorithm(co_r, mut_r):
    """
    Simulate running a GA for scheduling.
    In a real case, this would call your GA optimizer.
    """
    programs = ["Wildlife Documentary", "News", "Kids Show", "Sports Live", "Cooking Show", "Drama Series"]
    time_slots = ["08:00 AM", "09:00 AM", "10:00 AM", "11:00 AM", "12:00 PM", "01:00 PM"]

    # Shuffle to simulate GA optimization result
    random.seed(int(co_r * 1000 + mut_r * 10000))
    random.shuffle(programs)

    schedule = pd.DataFrame({
        "Time Slot": time_slots,
        "Program": programs
    })
    return schedule

# --- Run Button ---
if st.button("Run Genetic Algorithm"):
    st.success(f"✅ Genetic Algorithm executed with CO_R={co_r} and MUT_R={mut_r}")

    # Get schedule result
    schedule_df = run_genetic_algorithm(co_r, mut_r)

    st.subheader("📅 Optimized Program Schedule")
    st.dataframe(schedule_df, use_container_width=True)

    # Optionally export
    csv = schedule_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Schedule as CSV",
        data=csv,
        file_name="optimized_schedule.csv",
        mime="text/csv"
    )
else:
    st.info("Adjust parameters in the sidebar and click **Run Genetic Algorithm** to generate a schedule.")
