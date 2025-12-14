import pandas as pd
import random

# Static city coordinates (no API calls)
CITY_COORDS = {
    "Bangalore": {"lat": 12.9716, "lon": 77.5946},
    "Jaipur": {"lat": 26.9124, "lon": 75.7873},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
}

CITIES = list(CITY_COORDS.keys())

def generate_incidents(n=20):
    incidents = []
    status = ['Resolved', 'Pending', 'Escalated']

    for i in range(n):
        city = random.choice(CITIES)
        base = CITY_COORDS[city]

        incidents.append({
            "Flight": f"AI{100+i}",
            "Issue Type": random.choice(['Crew', 'Aircraft', 'Passenger', 'Weather']),
            "Status": random.choice(status),
            "Agent Action": random.choice([
                'Rebooked', 'Allocated Crew', 'Booked Hotel', 'Notification Sent'
            ]),
            "Escalated": random.choice(['Yes', 'No']),
            "City": city,
            "Latitude": base["lat"] + random.uniform(-0.15, 0.15),
            "Longitude": base["lon"] + random.uniform(-0.15, 0.15),
            "Passengers Affected": random.randint(5, 50)
        })

    return pd.DataFrame(incidents)

# Generate once
incidents_df = generate_incidents()
