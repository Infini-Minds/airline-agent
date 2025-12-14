import streamlit as st
from data.dummy_data import incidents_df

def show():
    st.title("📩 Notifications / Alerts")
    st.markdown("""
    **Purpose:**  
    Shows all proactive notifications sent to passengers affected by incidents, 
    including booking changes, hotel arrangements, or voucher issuance.
    """)
    st.subheader("Proactive Notifications Sent")
    notif_df = incidents_df[['Flight','Agent Action','Escalated','Passengers Affected']]
    st.dataframe(notif_df)
    st.markdown("✅ Notifications are sent automatically by the agent for resolved incidents.")
