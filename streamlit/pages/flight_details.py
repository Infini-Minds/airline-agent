import streamlit as st
from data.dummy_data import incidents_df

def show():
    st.title("✈️ Flight / Incident Details")
    st.markdown("""
    **Purpose:**  
    View detailed incident timelines for each flight. 
    Shows all agent actions, status updates, and whether the incident was escalated.
    """)
    flight_choice = st.selectbox("Select Flight", incidents_df['Flight'].unique())
    flight_details = incidents_df[incidents_df['Flight'] == flight_choice]
    
    st.subheader("Incident Timeline")
    for idx, row in flight_details.iterrows():
        st.markdown(f"- **Issue Type:** {row['Issue Type']} | **Status:** {row['Status']} | **Agent Action:** {row['Agent Action']} | **Escalated:** {row['Escalated']}")
