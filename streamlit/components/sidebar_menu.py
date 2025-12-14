import streamlit as st

def render_sidebar():
    st.markdown("<h2 style='text-align:center;color:#4B0082'>✈ Airline Ops</h2>", unsafe_allow_html=True)
    st.markdown("---")
    
    tabs = ["Dashboard", "Flight/Incident Details", "Notifications", "Analytics", "Bookings & Vouchers"]

    
    selected_tab = st.radio(
        "Navigate", 
        tabs, 
        index=0,
        label_visibility="collapsed"
    )
    
    # Add animated emojis next to tab
    if selected_tab == "Dashboard":
        st.markdown("🟢 Current Tab")
    elif selected_tab == "Flight/Incident Details":
        st.markdown("🟡 Inspect Flights")
    elif selected_tab == "Notifications":
        st.markdown("📩 Notifications Sent")
    elif selected_tab == "Analytics":
        st.markdown("📊 Analytics Overview")
        
    st.markdown("---")
    return selected_tab
