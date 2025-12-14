import pdfplumber
import pandas as pd

def extract_incidents_from_pdf(uploaded_file):
    try:
        with pdfplumber.open(uploaded_file) as pdf:
            text = "\n".join([page.extract_text() or "" for page in pdf.pages])
    except:
        return None

    incidents = []
    for line in text.split("\n"):
        lower = line.lower()
        if "delay" in lower or "cancel" in lower or "incident" in lower:
            incidents.append({
                "Flight": "Unknown",
                "Issue Type": line.strip(),
                "Status": "Detected",
                "Agent Action": "Pending",
                "Escalated": "No",
                "Passengers Affected": 0,
                "latitude": 12.97,     # dummy defaults for map
                "longitude": 77.59,
            })

    if not incidents:
        return None

    return pd.DataFrame(incidents)
