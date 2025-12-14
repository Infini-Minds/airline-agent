import streamlit as st
import pandas as pd
from components.kpi_cards import render_kpis
from components.animated_map import render_map
from data.dummy_data import incidents_df
from utils.pdf_incident_extractor import extract_incidents_from_pdf

def show():
    st.title("🛫 Airline Operations Dashboard")

    st.markdown("""
        **Overview:**  
        Live operational snapshot including:
        - Total incidents  
        - Automated agent actions  
        - Escalations  
        - Passengers impacted  
        - Real-time animated incident map  
        """)

    st.divider()

    # ---------------------------
    # UPLOAD PDF — INCIDENT DETECTION
    # ---------------------------
    st.subheader("📄 Upload PDF to Detect New Incidents")

    uploaded = st.file_uploader("Upload an Incident PDF Report", type=["pdf"])

    global incidents_df
    new_incidents_df = None

    if uploaded:
        with st.spinner("Extracting incidents..."):
            new_incidents_df = extract_incidents_from_pdf(uploaded)

        if new_incidents_df is not None and len(new_incidents_df) > 0:
            st.success(f"Detected {len(new_incidents_df)} new incidents!")

            # Show extracted
            st.write("### 🔍 Extracted Incidents from PDF")
            st.dataframe(new_incidents_df, width='stretch')

            # Merge with existing dashboard data
            incidents_df = pd.concat([incidents_df, new_incidents_df], ignore_index=True)
        else:
            st.warning("No incidents found in this PDF.")

    st.divider()

    # ---------------------------
    # KPIs
    # ---------------------------
    kpis = {
        "Total Incidents": len(incidents_df),
        "Automated Actions": len(incidents_df),
        "Escalated": len(incidents_df[incidents_df['Escalated'] == 'Yes']),
        "Passengers Affected": incidents_df["Passengers Affected"].sum(),
    }
    render_kpis(kpis)

    st.divider()

    # ---------------------------
    # Animated Flight Map
    # ---------------------------
    st.subheader("🌍 Real-Time Incident Map")
    render_map(incidents_df)

    st.divider()

    # ---------------------------
    # Incident Feed Table
    # ---------------------------
    st.subheader("📌 Incident Feed")
    st.dataframe(
        incidents_df[
            ["Flight", "Issue Type", "Status", "Agent Action", "Escalated", "Passengers Affected"]
        ],
        use_container_width=True,
    )
