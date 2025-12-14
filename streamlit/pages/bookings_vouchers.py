import streamlit as st
import pandas as pd
import random
from data.dummy_data import incidents_df

# Generate dummy booking & voucher data
def generate_booking_vouchers(df):
    data = []
    for idx, row in df.iterrows():
        num_passengers = row['Passengers Affected']
        for i in range(num_passengers):
            data.append({
                "Flight": row['Flight'],
                "City": row['City'],
                "Passenger ID": f"{row['Flight']}_P{i+1}",
                "Booking Status": random.choice(["Rebooked", "Cancelled", "Confirmed"]),
                "Voucher Issued": random.choice(["Hotel", "Food", "Travel Credit", "None"])
            })
    return pd.DataFrame(data)

booking_voucher_df = generate_booking_vouchers(incidents_df)

def show():
    st.title("🎫 Bookings & Vouchers")

    st.markdown("""
    **Purpose:**  
    Track passenger bookings affected by incidents and view all vouchers issued, 
    including hotels, meals, and travel credits.  
    Filter by flight or city to focus on specific operations.
    """)
    
    # Filters
    flight_filter = st.selectbox("Filter by Flight", ["All"] + booking_voucher_df['Flight'].unique().tolist())
    city_filter = st.selectbox("Filter by City", ["All"] + booking_voucher_df['City'].unique().tolist())
    
    filtered_df = booking_voucher_df.copy()
    if flight_filter != "All":
        filtered_df = filtered_df[filtered_df['Flight'] == flight_filter]
    if city_filter != "All":
        filtered_df = filtered_df[filtered_df['City'] == city_filter]
    
    st.subheader("Passenger Bookings & Vouchers")
    st.dataframe(filtered_df)
    
    # Summary KPIs
    total_bookings = len(filtered_df)
    total_vouchers = len(filtered_df[filtered_df['Voucher Issued'] != "None"])
    
    col1, col2 = st.columns(2)
    col1.metric("Total Bookings", total_bookings)
    col2.metric("Vouchers Issued", total_vouchers)
