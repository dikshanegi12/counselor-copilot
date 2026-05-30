"""
Counselor Co-Pilot — Streamlit UI

A demo interface showing how AI can help counselors prepare for student
conversations using existing student data systems.

⚠️ This demo uses SYNTHETIC data only. Never upload real student PII.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Make the src/ folder importable
sys.path.append(str(Path(__file__).parent / "src"))
from summarize import summarize_student  # change to "summarizer" if your file is named that


# ---------- Page config ----------
st.set_page_config(
    page_title="Counselor Co-Pilot",
    page_icon="🎓",
    layout="wide",
)

# ---------- Header ----------
st.title("🎓 Counselor Co-Pilot")
st.caption(
    "An AI-assisted prep tool for K-12 counselors. "
    "Upload student data, click a student, get a counselor-ready brief in seconds."
)

st.warning(
    "⚠️ **Demo only.** This prototype uses synthetic data. "
    "Never upload real student PII into experimental tools. "
    "Production use requires FERPA-compliant infrastructure and NIST AI RMF review."
)

# ---------- Sidebar: data source ----------
st.sidebar.header("Data source")

default_path = Path(__file__).parent / "data" / "sample_students.csv"
use_sample = st.sidebar.toggle("Use built-in sample data", value=True)

if use_sample:
    if default_path.exists():
        df = pd.read_csv(default_path)
        st.sidebar.success(f"Loaded {len(df)} synthetic students")
    else:
        st.sidebar.error("Sample data not found. Run data_generator.py first.")
        st.stop()
else:
    uploaded = st.sidebar.file_uploader("Upload a CSV", type="csv")
    if uploaded is None:
        st.sidebar.info("Upload a CSV to continue.")
        st.stop()
    df = pd.read_csv(uploaded)

# ---------- Main layout ----------
col_left, col_right = st.columns([1, 1.3])

with col_left:
    st.subheader("📋 Student roster")
    st.dataframe(df, use_container_width=True, height=420)

    # Quick filter
    grade_filter = st.selectbox(
        "Filter by grade", ["All"] + sorted(df["grade"].unique().tolist())
    )
    filtered = df if grade_filter == "All" else df[df["grade"] == grade_filter]

    # Pick a student
    student_label = st.selectbox(
        "Select a student to generate a brief",
        filtered.apply(
            lambda r: f"{r['student_id']} — {r['first_name']} {r['last_name']} (G{r['grade']})",
            axis=1,
        ).tolist(),
    )

with col_right:
    st.subheader("🤖 AI-generated counselor brief")

    if st.button("Generate brief", type="primary"):
        student_id = student_label.split(" — ")[0]
        student = df[df["student_id"] == student_id].iloc[0].to_dict()

        with st.spinner("Generating brief... (~10–20 seconds)"):
            brief = summarize_student(student)

        st.markdown("### Brief")
        st.write(brief)

        with st.expander("📊 See the underlying data"):
            st.json(student)

        st.caption(
            "⚠️ AI-generated. Always review for accuracy before acting. "
            "This tool augments counselor judgment, it does not replace it."
        )
    else:
        st.info("👈 Select a student and click **Generate brief** to start.")

# ---------- Footer ----------
st.divider()
st.caption(
    "Built as a prototype to explore AI augmentation in K-12 advising workflows. "
    "Designed with NIST AI RMF principles in mind: transparency, human oversight, "
    "and minimization of risk to students."
)