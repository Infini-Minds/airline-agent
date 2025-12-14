import streamlit as st
from pages import (
    dashboard,
    flight_details,
    notifications,
    analytics,
    bookings_vouchers,
    incident_detector   # <-- NEW PAGE
)
from components.sidebar_menu import render_sidebar

# Page config
st.set_page_config(page_title="Airline Ops Dashboard", layout="wide")

# Sidebar menu
selected_tab = render_sidebar()

# Router
if selected_tab == "Dashboard":
    dashboard.show()
elif selected_tab == "Flight/Incident Details":
    flight_details.show()
elif selected_tab == "Notifications":
    notifications.show()
elif selected_tab == "Analytics":
    analytics.show()
elif selected_tab == "Bookings & Vouchers":
    bookings_vouchers.show()
elif selected_tab == "Incident Detector":     # <-- NEW ROUTE
    incident_detector.show()
