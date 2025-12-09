import os
import streamlit as st
import requests

st.title("❤️ Heart Disease Prediction App (FastAPI Backend)")
st.write("Enter patient details and get prediction from FastAPI backend.")

# -----------------------------
# USER INPUTS
# -----------------------------

age = st.slider("Age", 20, 80, 50)
resting_bp = st.number_input("Resting Blood Pressure (mmHg)", 80, 200, 120)
cholesterol = st.number_input("Cholesterol (mg/dL)", 100, 600, 200)
fasting_bs = st.selectbox("Fasting Blood Sugar > 120 mg/dL", ["No", "Yes"])
fasting_bs = 1 if fasting_bs == "Yes" else 0
max_hr = st.number_input("Maximum Heart Rate Achieved", 60, 220, 150)
oldpeak = st.number_input("Oldpeak (ST Depression)", -3.0, 7.0, 1.0, step=0.1)

sex = st.radio("Sex", ["Male", "Female"])
cp = st.selectbox("Chest Pain Type", ["ATA", "NAP", "TA", "ASY"])
restecg = st.selectbox("Resting ECG", ["Normal", "ST", "LVH"])
angina = st.radio("Exercise-Induced Angina", ["Yes", "No"])
slope = st.selectbox("ST Slope", ["Up", "Flat", "Down"])

# -----------------------------
# JSON Payload for FastAPI
# -----------------------------

payload = {
    "Age": age,
    "RestingBP": resting_bp,
    "Cholesterol": cholesterol,
    "FastingBS": fasting_bs,
    "MaxHR": max_hr,
    "Oldpeak": oldpeak,
    "Sex": sex,
    "ChestPainType": cp,
    "RestingECG": restecg,
    "ExerciseAngina": angina,
    "ST_Slope": slope
}

# -----------------------------
# Call FastAPI
# -----------------------------

# get backend url from environment or secrets
BACKEND_URL = "https://heart-api-wb2j.onrender.com/predict"

if st.button("Predict"):
    with st.spinner("Sending data to FastAPI backend..."):
        try:
            response = requests.post(BACKEND_URL, json=payload, timeout=10)

            if response.status_code == 200:
                result = response.json()

                prediction = result["prediction"]
                probability = result["probability"]

                st.subheader("🔍 Prediction Result:")

                if prediction == 1:
                    st.error(f"❗ High Risk of Heart Disease\nProbability: {probability:.2f}")
                else:
                    st.success(f"✅ No Heart Disease Detected\nProbability: {probability:.2f}")

            else:
                st.warning("⚠️ FastAPI returned an error. Check backend.")

        except Exception as e:
            st.error(f"❌ Error connecting to FastAPI: {e}")

