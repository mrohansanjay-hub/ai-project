import pandas as pd
import pickle
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestClassifier

df = pd.read_csv("soil_health.csv")

X = df[
    ["nitrogen", "phosphorus", "potassium", "ph", "moisture", "ec", "temperature"]
]
y = df["soil_health"]

pipeline = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(
        n_estimators=200,
        max_depth=6,
        min_samples_split=5,
        random_state=42
    ))
])

pipeline.fit(X, y)

with open("../models/soil_health.pkl", "wb") as f:
    pickle.dump(pipeline, f)

print("✅ ML model trained and saved")
