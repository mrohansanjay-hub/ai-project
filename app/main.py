from fastapi import FastAPI
import pickle

from app.schemas import SoilInput
from app.rules import classify_soil_health, apply_rules
from app.reasoning import generate_reasoning

app = FastAPI(title="AI Soil Advisor")

with open("models/soil_health.pkl", "rb") as f:
    ml_model = pickle.load(f)

@app.post("/ai/soil/analyze")
def analyze_soil(data: SoilInput):

    ml_features = [[
        data.nitrogen,
        data.phosphorus,
        data.potassium,
        data.ph,
        data.moisture,
        data.ec,
        data.temperature
    ]]

    ml_prediction = int(ml_model.predict(ml_features)[0])

    soil_health, issues = classify_soil_health(data)
    actions, warnings = apply_rules(data)

    reasoning = generate_reasoning(
        data,
        soil_health,
        issues,
        actions,
        warnings
    )

    return {
        "soil_health": soil_health,
        "ml_prediction_class": ml_prediction,
        "reasoning": reasoning,
        "raw_input": data.dict()
    }
