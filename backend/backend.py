from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import pandas as pd
import os

app = FastAPI(title="Heart Disease Prediction API")

# Load model, scaler, columns (paths relative to file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "LR_heart_model.pkl")
SCALER_PATH = os.path.join(BASE_DIR, "heart_scaler.pkl")
COLS_PATH = os.path.join(BASE_DIR, "heart_columns.pkl")

model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)
columns = joblib.load(COLS_PATH)

# Input schema
class HeartInput(BaseModel):
    Age: int
    RestingBP: int
    Cholesterol: int
    FastingBS: int
    MaxHR: int
    Oldpeak: float
    Sex: str
    ChestPainType: str
    RestingECG: str
    ExerciseAngina: str
    ST_Slope: str

@app.get("/")
def root():
    return {"status": "ok", "message": "Heart Disease API running."}

@app.post("/predict")
def predict_heart(data: HeartInput):
    # Map categorical fields
    sex_m = 1 if data.Sex == "Male" else 0

    cp_ata = 1 if data.ChestPainType == "ATA" else 0
    cp_nap = 1 if data.ChestPainType == "NAP" else 0
    cp_ta = 1 if data.ChestPainType == "TA" else 0

    restecg_normal = 1 if data.RestingECG == "Normal" else 0
    restecg_st = 1 if data.RestingECG == "ST" else 0

    angina_y = 1 if data.ExerciseAngina == "Yes" else 0

    st_slope_flat = 1 if data.ST_Slope == "Flat" else 0
    st_slope_up = 1 if data.ST_Slope == "Up" else 0

    # Age groups
    if data.Age < 40:
        age_mid = 0
        age_senior = 0
    elif 40 <= data.Age < 55:
        age_mid = 1
        age_senior = 0
    else:
        age_mid = 0
        age_senior = 1

    # Create input dataframe
    row = pd.DataFrame([{ 
        'Age': data.Age,
        'RestingBP': data.RestingBP,
        'Cholesterol': data.Cholesterol,
        'FastingBS': data.FastingBS,
        'MaxHR': data.MaxHR,
        'Oldpeak': data.Oldpeak,
        'HeartDisease': 0,
        'Sex_M': sex_m,
        'ChestPainType_ATA': cp_ata,
        'ChestPainType_NAP': cp_nap,
        'ChestPainType_TA': cp_ta,
        'RestingECG_Normal': restecg_normal,
        'RestingECG_ST': restecg_st,
        'ExerciseAngina_Y': angina_y,
        'ST_Slope_Flat': st_slope_flat,
        'ST_Slope_Up': st_slope_up,
        'AgeGroup_Middle-aged': age_mid,
        'AgeGroup_Senior': age_senior
    }])

    # ensure columns order
    row = row[columns]

    # scale
    scaled = scaler.transform(row)
    pred = int(model.predict(scaled)[0])
    proba = float(model.predict_proba(scaled)[0][1]) if hasattr(model, "predict_proba") else None

    return {"prediction": pred, "probability": proba}
