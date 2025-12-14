# api_client.py

import streamlit as st
import requests

BASE_URL = "http://localhost:5000"

def fetch_data(endpoint: str):
    """Fetches data from the specified API endpoint."""
    try:
        response = requests.get(f"{BASE_URL}{endpoint}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.ConnectionError:
        # Silently fail on connection errors to keep the dashboard loop running
        return None
    except requests.exceptions.RequestException as e:
        # st.error(f"API Error fetching {endpoint}: {e}") # Suppress this error to avoid flooding the UI
        return None

def post_threat_simulation(city: str, alternate_airport: str | None) -> dict | str:
    """Posts a bomb threat to the Flask API."""
    try:
        # Use query parameters as defined in your Flask app
        params = {"city": city}
        if alternate_airport:
            params["alternate_airport"] = alternate_airport
            
        response = requests.post(f"{BASE_URL}/bomb-threat/city", params=params)
        
        # Check for HTTP errors (4xx or 5xx)
        response.raise_for_status()
        
        # Success case
        return f"Threat successfully simulated in **{city}**!"
    
    except requests.exceptions.HTTPError as e:
        # Handle specific API errors from the Flask app
        try:
            error_data = response.json()
            return error_data
        except:
            return {"error": f"HTTP Error {response.status_code}: {e}"}
            
    except requests.exceptions.RequestException as e:
        return {"error": f"Connection or unexpected error: {e}"}