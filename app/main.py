from fastapi import FastAPI, HTTPException
import pickle
import pandas as pd

from app.schemas import SoilInput
from app.rules import classify_soil_health
from app.reasoning import generate_reasoning
from app.fertilizer_calculator import calculate_fertilizer
from app.weather_service import get_weather

app = FastAPI(title="AI Soil Advisor")

# -------- Load ML Model --------
try:
    with open("models/soil_health.pkl", "rb") as f:
        ml_model = pickle.load(f)
except Exception as e:
    raise RuntimeError(f"Failed to load ML model: {e}")


# -------- HARD INPUT VALIDATION --------
def validate_soil_input(data: SoilInput):
    errors = []

    if data.nitrogen <= 0:
        errors.append("Invalid nitrogen value")
    if data.phosphorus <= 0:
        errors.append("Invalid phosphorus value")
    if data.potassium <= 0:
        errors.append("Invalid potassium value")
    if not (3.5 <= data.ph <= 9.5):
        errors.append("Invalid pH value")
    if data.moisture <= 0:
        errors.append("Invalid moisture value")
    if data.temperature < 5:
        errors.append("Invalid temperature value")

    if errors:
        return False, errors

    return True, None


@app.post("/ai/soil/analyze")
def analyze_soil(data: SoilInput):
    """
    End-to-end soil + weather + AI reasoning endpoint
    """

    # -------- STOP IF INPUT INVALID --------
    is_valid, errors = validate_soil_input(data)
    if not is_valid:
        return {
            "error": "Insufficient or invalid soil data",
            "details": errors
        }

    crop_name = data.crop.lower()

    # -------- Weather Data --------
    try:
        weather = get_weather(
            latitude=data.latitude,
            longitude=data.longitude
        )
    except Exception:
        weather = {
            "today_temp": None,
            "rain_probability": None,
            "warning": "Weather data unavailable"
        }

    # -------- ML Prediction (FIXED) --------
    feature_columns = [
        "nitrogen",
        "phosphorus",
        "potassium",
        "ph",
        "moisture",
        "ec",
        "temperature"
    ]

    ml_features = pd.DataFrame([{
        "nitrogen": data.nitrogen,
        "phosphorus": data.phosphorus,
        "potassium": data.potassium,
        "ph": data.ph,
        "moisture": data.moisture,
        "ec": data.ec,
        "temperature": data.temperature
    }], columns=feature_columns)

    try:
        ml_prediction_class = int(ml_model.predict(ml_features)[0])
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"ML prediction failed: {e}"
        )

    ml_label_map = {
        0: "Poor",
        1: "Moderate",
        2: "Good"
    }

    ml_prediction_label = ml_label_map.get(
        ml_prediction_class, "Unknown"
    )

    # -------- Rule-Based Soil Health --------
    soil_class, soil_label, issues = classify_soil_health(data)

    # -------- Fertilizer Recommendation (FIXED) --------
    fertilizer = calculate_fertilizer(
        data=data,
        crop=crop_name
    )

    # -------- Weather Warnings --------
    warnings = []
    if weather.get("rain_probability") is not None:
        if weather["rain_probability"] < 20:
            warnings.append(
                "Low rainfall expected – irrigate before fertilizer application"
            )

    # -------- AI Reasoning --------
    reasoning = generate_reasoning(
        data=data,
        soil_health=soil_label,
        issues=issues,
        actions=[],
        warnings=warnings,
        weather=weather
    )

    # -------- Final Response --------
    return {
        "soil_health": soil_label,
        "ml_prediction_class": ml_prediction_class,
        "ml_prediction_label": ml_prediction_label,
        "weather": weather,
        "fertilizer": fertilizer,
        "warnings": warnings,
        "reasoning": reasoning,
        "raw_input": data.dict()
    }
