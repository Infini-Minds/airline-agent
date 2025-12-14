import streamlit as st
from data.dummy_data import incidents_df

def show():
    st.title("📊 Analytics / Reports")
    st.markdown("""
    **Purpose:**  
    Analyze trends in incidents, agent actions, and escalation rates.  
    Provides insights for operational efficiency and proactive decision-making.
    """)

    
    # Incident Status Distribution
    st.subheader("Incident Trends")
    status_counts = incidents_df['Status'].value_counts()
    st.bar_chart(status_counts)
    
    # Agent Actions
    st.subheader("Agent Action Distribution")
    action_counts = incidents_df['Agent Action'].value_counts()
    st.bar_chart(action_counts)
    
    # Escalation Rate
    st.subheader("Escalation Rate")
    escalated_count = len(incidents_df[incidents_df['Escalated']=='Yes'])
    total_incidents = len(incidents_df)
    escalated_rate = escalated_count / total_incidents * 100
    st.metric("Escalation Rate (%)", f"{escalated_rate:.2f}%")
