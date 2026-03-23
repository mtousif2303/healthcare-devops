import streamlit as st
import pandas as pd
import requests
import random
from datetime import datetime, timedelta

# -------------------------
# Fetch patient data
# -------------------------
def fetch_patients():
    try:
        response = requests.get("https://randomuser.me/api/?results=50")
        response.raise_for_status()
        return response.json()["results"]
    except Exception:
        return []

# -------------------------
# Generate healthcare services
# -------------------------
def generate_healthcare_data(num_records):
    services = ["General Checkup", "Blood Test", "X-Ray", "MRI", "Surgery"]
    data = []

    for _ in range(num_records):
        data.append({
            "service_id": random.randint(1000, 9999),
            "service_name": random.choice(services),
            "service_cost": round(random.uniform(50, 1000), 2),
            "service_date": (
                datetime.now() - timedelta(days=random.randint(0, 365))
            ).strftime("%Y-%m-%d"),
        })

    return pd.DataFrame(data)

# -------------------------
# Generate medication data
# -------------------------
def generate_medication_data(num_records):
    medications = ["Paracetamol", "Ibuprofen", "Aspirin", "Metformin", "Amoxicillin"]
    data = []

    for _ in range(num_records):
        data.append({
            "medication_id": random.randint(1000, 9999),
            "medication_name": random.choice(medications),
            "dosage": f"{random.randint(1, 500)} mg",
            "medication_cost": round(random.uniform(10, 200), 2),
            "prescribed_date": (
                datetime.now() - timedelta(days=random.randint(0, 365))
            ).strftime("%Y-%m-%d"),
        })

    return pd.DataFrame(data)

# -------------------------
# Fetch facility data
# -------------------------
def fetch_facilities():
    try:
        response = requests.get("https://health.data.ny.gov/resource/xdss-u53e.json")
        response.raise_for_status()
        return pd.DataFrame(response.json())
    except Exception:
        return pd.DataFrame()

# -------------------------
# Transform patient data
# -------------------------
def transform_patients(data):
    patients = []

    for patient in data:
        patients.append({
            "patient_id": patient["login"]["uuid"],
            "name": f"{patient['name']['first']} {patient['name']['last']}",
            "email": patient["email"],
            "age": patient["dob"]["age"],
            "gender": patient["gender"],
            "phone": patient["phone"],
            "city": patient["location"]["city"],
            "country": patient["location"]["country"],
        })

    return pd.DataFrame(patients)

# -------------------------
# Assign services
# -------------------------
def assign_services_to_patients(patients, services):
    service_ids = services["service_id"].tolist()
    patients["service_id"] = [random.choice(service_ids) for _ in range(len(patients))]
    return patients.merge(services, on="service_id")

# -------------------------
# Assign medications
# -------------------------
def assign_medications_to_patients(patients, medications):
    medication_ids = medications["medication_id"].tolist()
    patients["medication_id"] = [
        random.choice(medication_ids) for _ in range(len(patients))
    ]
    return patients.merge(medications, on="medication_id")

# -------------------------
# Main Dashboard
# -------------------------
def main():

    st.set_page_config(page_title="Healthcare Data Pipeline", layout="wide")

    st.title("Real-Time Healthcare Data Pipeline Dashboard")

    st.write(
        "This dashboard simulates a **real-time CI/CD healthcare data pipeline** "
        "showing patient services, medication usage, and healthcare facilities."
    )

    st.subheader("Real-Time Data Refresh")

    if st.button("Refresh Data"):
        st.rerun()

    # Fetch data
    patients_data = fetch_patients()
    healthcare_data = generate_healthcare_data(100)
    medication_data = generate_medication_data(100)
    facilities_data = fetch_facilities()

    # Transform
    patients_df = transform_patients(patients_data)

    # Join datasets
    patients_services_df = assign_services_to_patients(patients_df, healthcare_data)
    merged_df = assign_medications_to_patients(patients_services_df, medication_data)

    # -------------------------
    # Display Tables
    # -------------------------

    st.subheader("Patients Data")
    st.dataframe(patients_df)

    st.subheader("Healthcare Services Data")
    st.dataframe(healthcare_data)

    st.subheader("Medication Data")
    st.dataframe(medication_data)

    st.subheader("Healthcare Facilities Data")
    st.dataframe(facilities_data.head(20))

    st.subheader("Merged Patient Data")
    st.dataframe(merged_df)

    st.subheader("Data Summary")
    st.dataframe(merged_df.describe())

    # -------------------------
    # Charts
    # -------------------------

    st.subheader("Service Cost Distribution")
    st.bar_chart(merged_df["service_cost"])

    st.subheader("Medication Cost Distribution")
    st.bar_chart(merged_df["medication_cost"])

    st.subheader("Service Count by Type")
    service_count = merged_df["service_name"].value_counts()
    st.bar_chart(service_count)

    st.subheader("Medication Cost Over Time")
    medication_cost_over_time = (
        merged_df.groupby("prescribed_date")["medication_cost"].sum().reset_index()
    )
    st.line_chart(medication_cost_over_time.set_index("prescribed_date"))

# -------------------------
# Run App
# -------------------------
if __name__ == "__main__":
    main()