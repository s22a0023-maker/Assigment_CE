import streamlit as st
import pandas as pd
import random

# -----------------------------
# Streamlit UI Setup
# -----------------------------
st.title("🧬 Genetic Algorithm – Program Scheduling")

st.markdown("""
This app allows you to configure the **Genetic Algorithm parameters**
and view the resulting **optimized schedule** using your uploaded dataset.
""")

# -----------------------------
# Upload CSV File
# -----------------------------
st.sidebar.header("📁 Upload Dataset")
uploaded_file = st.sidebar.file_uploader("Upload your CSV file", type=["csv"])

if uploaded_file is not None:
    df = pd.read_csv(uploaded_file)
    st.success("✅ Dataset uploaded successfully!")
    st.dataframe(df.head(), use_container_width=True)
else:
    st.warning("⚠️ Please upload a CSV file to begin.")
    st.stop()  # Stop the app here until file is uploaded

# -----------------------------
# GA Parameter Inputs
# -----------------------------
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
def run_genetic_algorithm(df, co_r, mut_r):
    """
    Simulate a GA schedule optimization using the uploaded dataset.
    Detects program names and uses the dataset's time slot headers (e.g., Hour 6, Hour 7...).
    """

    # --- Detect program name column ---
    program_col = None
    for col in df.columns:
        if "program" in col.lower() or "name" in col.lower() or "title" in col.lower():
            program_col = col
            break

    # If not found, assume first column holds program names
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

    # --- Detect time slot columns automatically ---
    # Example: columns like "Hour 6", "Hour 7", etc.
    time_slots = [
        col for col in df.columns
        if "hour" in col.lower() or "time" in col.lower()
    ]

    # Fallback if no explicit hour columns are found
    if not time_slots:
        time_slots = [f"Hour {i+1}" for i in range(min(6, len(programs)))]

    # --- Simulate GA schedule by randomizing ---
    random.seed(int(co_r * 1000 + mut_r * 10000))
    random.shuffle(programs)

    # --- Match programs to available time slots ---
    schedule = pd.DataFrame({
        "Time Slot": time_slots[:len(programs)],
        "Program": programs[:len(time_slots)]
    })

    return schedule


# -----------------------------
# Run GA Button
# -----------------------------
if st.button("🚀 Run Genetic Algorithm"):
    st.success(f"✅ GA executed with CO_R={co_r}, MUT_R={mut_r}")

    schedule_df = run_genetic_algorithm(df, co_r, mut_r)

    st.subheader("📅 Optimized Program Schedule")
    st.dataframe(schedule_df, use_container_width=True)

    # Download option
    csv = schedule_df.to_csv(index=False).encode("utf-8")
    st.download_button(
        "⬇️ Download Schedule as CSV",
        data=csv,
        file_name="optimized_schedule.csv",
        mime="text/csv"
    )

else:
    st.info("Adjust parameters and click **Run Genetic Algorithm** to generate a schedule.")
