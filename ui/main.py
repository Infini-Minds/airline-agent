# app.py

import streamlit as st
import time
import pandas as pd
import requests

# Import helper functions and API client
from dashboard_utils import (
    render_summary_metrics,
    render_map_view,
    render_incident_feed,
    render_analytics,
    convert_df_to_csv,
)
from api_client import fetch_data, post_threat_simulation

# --- Configuration and Helpers ---
st.set_page_config(
    page_title="Airline Threat Monitor Dashboard",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Colors (for sidebar use)
CRITICAL_COLOR = "#FF4B4B"

# Initialize Session State for Filters
if "filter_flight" not in st.session_state:
    st.session_state["filter_flight"] = ""
if "filter_status" not in st.session_state:
    st.session_state["filter_status"] = "All"


def main():
    """Main application function."""
    st.title("🚨 Airline Crisis Management")
    st.markdown(
        "A real-time monitor for flight disruptions and automated threat responses."
    )

    # 1. Sidebar with Operational Status and Legend (CLEANED)
    with st.sidebar:
        # 1. Status Indicator
        st.markdown(
            f"""
            <h1 style='color: {CRITICAL_COLOR};'>
                <i class="fas fa-exclamation-triangle"></i> ALERT
            </h1>
            <p>Operational Status: <b>Real-Time Monitoring</b></p>
            """,
            unsafe_allow_html=True,
        )
        st.markdown("---")

        # 2. Map Legend / Status Keys
        st.caption("Map Legend & Status Keys")
        st.markdown(
            f"""
            <div style="font-size: 14px; padding-left: 10px;">
                <p><span style="color: red;">&#9679;</span> - High Severity Incident (e.g., Threat)</p>
                <p><span style="color: orange;">&#9679;</span> - Medium Severity (e.g., Rerouted)</p>
                <p><span style="color: blue;">&#9679;</span> - Low Severity (e.g., Resolved)</p>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown("---")
        st.info("System operational and monitoring all 7,500 active flights.")

    # 2. Main Dashboard Layout (Real-time updates)
    dashboard_placeholder = st.empty()

    while True:
        with dashboard_placeholder.container():

            # Fetch all data concurrently
            incident_feed_data = fetch_data("/dashboard/summary")
            map_data = fetch_data("/dashboard/map")
            status_data = fetch_data("/analytics/status-distribution")
            escalation_rate = fetch_data("/analytics/escalation-rate")

            if incident_feed_data is None and map_data is None:
                st.warning(
                    "Waiting for API connection. Please ensure Flask server is running on port 5000."
                )
            else:
                # -----------------
                # SECTION A: SUMMARY
                # -----------------
                render_summary_metrics(incident_feed_data)

                col_map, col_details = st.columns([2, 1])

                with col_map:
                    render_map_view(map_data)

                with col_details:
                    render_analytics(status_data, escalation_rate)

                # -----------------
                # SECTION B: FILTERS & SEARCH (Prominent)
                # -----------------
                st.markdown("---")
                st.markdown("### 🔍 Incident Search & Filter")

                col_search, col_filter, col_download = st.columns([3, 2, 1])

                # Search Input
                with col_search:
                    flight_search = st.text_input(
                        "Search by Flight Number",
                        value=st.session_state["filter_flight"],
                        key="search_input_key",
                        placeholder="Enter flight ID (e.g., F1001)",
                    )
                    st.session_state["filter_flight"] = flight_search

                # Status Filter Selectbox
                with col_filter:
                    # Collect all unique statuses for the dropdown filter
                    try:
                        status_options = ["All"] + sorted(
                            pd.DataFrame(incident_feed_data)["Status"].unique().tolist()
                        )
                    except:
                        status_options = [
                            "All",
                            "Cancelled",
                            "Rerouted",
                            "Resolved",
                        ]  # Fallback

                    status_filter = st.selectbox(
                        "Filter by Status",
                        options=status_options,
                        key="status_select_key",
                    )
                    st.session_state["filter_status"] = status_filter

                # Download Button
                with col_download:
                    st.markdown("#### Download Feed")  # Label for alignment

                    full_df = (
                        pd.DataFrame(incident_feed_data)
                        if incident_feed_data
                        else pd.DataFrame()
                    )

                    # Apply Filtering Logic for Download
                    download_df = full_df.copy()
                    if st.session_state["filter_flight"]:
                        download_df = download_df[
                            download_df["Flight"].str.contains(
                                st.session_state["filter_flight"], case=False, na=False
                            )
                        ]
                    if st.session_state["filter_status"] != "All":
                        download_df = download_df[
                            download_df["Status"] == st.session_state["filter_status"]
                        ]

                    csv = convert_df_to_csv(download_df)

                    st.download_button(
                        label="Download Filtered Data (.csv)",
                        data=csv,
                        file_name="filtered_incident_feed.csv",
                        mime="text/csv",
                        use_container_width=True,
                        type="secondary",
                    )

                # -----------------
                # SECTION C: INCIDENT FEED
                # -----------------
                render_incident_feed(
                    incident_feed_data,
                    flight_filter=st.session_state["filter_flight"],
                    status_filter=st.session_state["filter_status"],
                )

        # 3. Animation and Refresh
        time.sleep(5)


if __name__ == "__main__":
    main()
