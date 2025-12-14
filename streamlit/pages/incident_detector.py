import streamlit as st
import pdfplumber

def show():
    st.title("Incident Detector (Upload PDF)")
    st.write("Upload a PDF to automatically extract incidents.")

    uploaded_file = st.file_uploader("Choose a PDF file", type=["pdf"])

    if uploaded_file:
        with pdfplumber.open(uploaded_file) as pdf:
            text = ""
            for page in pdf.pages:
                text += page.extract_text() + "\n"

        st.subheader("Extracted Text")
        st.text_area("PDF Content", text, height=300)

        # Dummy incident extraction logic
        incidents = []
        for line in text.split("\n"):
            if "delay" in line.lower() or "cancel" in line.lower() or "incident" in line.lower():
                incidents.append(line)

        st.subheader("Detected Incidents")
        if incidents:
            for i, inc in enumerate(incidents, 1):
                st.write(f"**{i}.** {inc}")
        else:
            st.info("No incidents found in the PDF.")
