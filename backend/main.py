"""
AI-Powered Flash Flood Prediction System — FastAPI Backend
Demonstration Prototype — Uses Synthetic Data
"""

import os
import joblib
import numpy as np
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import List, Optional

# ── App setup ──────────────────────────────────────────────────────────────────
app = FastAPI(
    title="Flash Flood Prediction API",
    description="Demonstration prototype — synthetic data only.",
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Load model ─────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "model", "flood_model.pkl")

payload       = joblib.load(MODEL_PATH)
clf           = payload["model"]
le            = payload["label_encoder"]
FEATURE_COLS  = payload["feature_cols"]
MODEL_METRICS = payload["metrics"]

# ── Static location data ───────────────────────────────────────────────────────
LOCATIONS = [
    {
        "id": "valley_a",
        "name": "Valley A",
        "lat": 27.42,
        "lng": 85.34,
        "elevation": 1240,
        "slope": 32,
        "drainage_density": 0.72,
        "description": "Low-lying valley between two ridgelines, high runoff potential.",
    },
    {
        "id": "valley_b",
        "name": "Valley B",
        "lat": 27.38,
        "lng": 85.41,
        "elevation": 980,
        "slope": 24,
        "drainage_density": 0.58,
        "description": "Agricultural valley with moderate drainage capacity.",
    },
    {
        "id": "hill_zone_c",
        "name": "Hill Zone C",
        "lat": 27.46,
        "lng": 85.28,
        "elevation": 1680,
        "slope": 48,
        "drainage_density": 0.85,
        "description": "Steep forested hillside with fast-draining channels.",
    },
    {
        "id": "river_zone_d",
        "name": "River Zone D",
        "lat": 27.35,
        "lng": 85.47,
        "elevation": 720,
        "slope": 15,
        "drainage_density": 0.90,
        "description": "River confluence zone, prone to rapid water-level rise.",
    },
    {
        "id": "mountain_zone_e",
        "name": "Mountain Zone E",
        "lat": 27.50,
        "lng": 85.22,
        "elevation": 1950,
        "slope": 55,
        "drainage_density": 0.65,
        "description": "High-altitude rocky terrain with exposed bare soil.",
    },
    {
        "id": "plateau_f",
        "name": "Plateau F",
        "lat": 27.32,
        "lng": 85.38,
        "elevation": 1150,
        "slope": 10,
        "drainage_density": 0.40,
        "description": "Flat plateau with urban land cover and poor natural drainage.",
    },
    {
        "id": "gorge_g",
        "name": "Gorge G",
        "lat": 27.44,
        "lng": 85.52,
        "elevation": 860,
        "slope": 38,
        "drainage_density": 0.78,
        "description": "Narrow gorge that channels floodwaters rapidly downstream.",
    },
]

# Scenario presets per location
# Each scenario defines the variable environmental conditions
SCENARIOS = {
    "normal": {
        "valley_a":      dict(rainfall_1h=8,  rainfall_3h=18,  rainfall_6h=28,  soil_moisture=0.28, antecedent_rainfall=20,  land_cover="forest"),
        "valley_b":      dict(rainfall_1h=6,  rainfall_3h=14,  rainfall_6h=22,  soil_moisture=0.32, antecedent_rainfall=18,  land_cover="agriculture"),
        "hill_zone_c":   dict(rainfall_1h=10, rainfall_3h=22,  rainfall_6h=34,  soil_moisture=0.22, antecedent_rainfall=25,  land_cover="forest"),
        "river_zone_d":  dict(rainfall_1h=5,  rainfall_3h=12,  rainfall_6h=18,  soil_moisture=0.35, antecedent_rainfall=15,  land_cover="grassland"),
        "mountain_zone_e":dict(rainfall_1h=12,rainfall_3h=26,  rainfall_6h=40,  soil_moisture=0.18, antecedent_rainfall=30,  land_cover="bare_soil"),
        "plateau_f":     dict(rainfall_1h=7,  rainfall_3h=16,  rainfall_6h=24,  soil_moisture=0.30, antecedent_rainfall=12,  land_cover="urban"),
        "gorge_g":       dict(rainfall_1h=9,  rainfall_3h=20,  rainfall_6h=30,  soil_moisture=0.25, antecedent_rainfall=22,  land_cover="forest"),
    },
    "heavy_rain": {
        # Calibrated so all locations land in MODERATE-to-HIGH band (35-79%)
        "valley_a":       dict(rainfall_1h=42, rainfall_3h=78,  rainfall_6h=118, soil_moisture=0.66, antecedent_rainfall=80,  land_cover="forest"),
        "valley_b":       dict(rainfall_1h=40, rainfall_3h=74,  rainfall_6h=112, soil_moisture=0.64, antecedent_rainfall=76,  land_cover="agriculture"),
        "hill_zone_c":    dict(rainfall_1h=45, rainfall_3h=84,  rainfall_6h=126, soil_moisture=0.65, antecedent_rainfall=84,  land_cover="forest"),
        "river_zone_d":   dict(rainfall_1h=38, rainfall_3h=70,  rainfall_6h=106, soil_moisture=0.63, antecedent_rainfall=72,  land_cover="grassland"),
        "mountain_zone_e":dict(rainfall_1h=44, rainfall_3h=82,  rainfall_6h=122, soil_moisture=0.64, antecedent_rainfall=82,  land_cover="bare_soil"),
        "plateau_f":      dict(rainfall_1h=41, rainfall_3h=76,  rainfall_6h=114, soil_moisture=0.65, antecedent_rainfall=78,  land_cover="urban"),
        "gorge_g":        dict(rainfall_1h=43, rainfall_3h=80,  rainfall_6h=120, soil_moisture=0.66, antecedent_rainfall=81,  land_cover="forest"),
    },
    "extreme_rain": {
        "valley_a":      dict(rainfall_1h=92, rainfall_3h=158, rainfall_6h=210, soil_moisture=0.88, antecedent_rainfall=155, land_cover="forest"),
        "valley_b":      dict(rainfall_1h=85, rainfall_3h=148, rainfall_6h=198, soil_moisture=0.90, antecedent_rainfall=145, land_cover="agriculture"),
        "hill_zone_c":   dict(rainfall_1h=98, rainfall_3h=168, rainfall_6h=225, soil_moisture=0.82, antecedent_rainfall=160, land_cover="forest"),
        "river_zone_d":  dict(rainfall_1h=80, rainfall_3h=140, rainfall_6h=188, soil_moisture=0.92, antecedent_rainfall=138, land_cover="grassland"),
        "mountain_zone_e":dict(rainfall_1h=105,rainfall_3h=178,rainfall_6h=238, soil_moisture=0.78, antecedent_rainfall=165, land_cover="bare_soil"),
        "plateau_f":     dict(rainfall_1h=88, rainfall_3h=152, rainfall_6h=202, soil_moisture=0.91, antecedent_rainfall=150, land_cover="urban"),
        "gorge_g":       dict(rainfall_1h=95, rainfall_3h=162, rainfall_6h=218, soil_moisture=0.85, antecedent_rainfall=158, land_cover="forest"),
    },
}

# ── Helpers ────────────────────────────────────────────────────────────────────

def classify_risk(probability: float) -> dict:
    """Convert flood probability [0–100] to risk level + warning."""
    if probability < 30:
        return {
            "risk_level": "LOW",
            "color": "green",
            "warning": None,
        }
    elif probability < 60:
        return {
            "risk_level": "MODERATE",
            "color": "yellow",
            "warning": "Moderate flood risk detected. Stay alert and monitor conditions.",
        }
    elif probability < 80:
        return {
            "risk_level": "HIGH",
            "color": "orange",
            "warning": "High flash flood risk. Prepare evacuation plans and follow emergency instructions.",
        }
    else:
        return {
            "risk_level": "SEVERE",
            "color": "red",
            "warning": "SEVERE flash flood risk. Immediate preparedness is required. Evacuate low-lying areas.",
        }


def get_contributing_factors(
    rainfall_1h, rainfall_3h, rainfall_6h,
    soil_moisture, slope, antecedent_rainfall,
    land_cover, drainage_density
) -> List[str]:
    factors = []
    if rainfall_1h > 50:
        factors.append("Very high 1-hour rainfall intensity")
    elif rainfall_1h > 25:
        factors.append("High 1-hour rainfall intensity")

    if rainfall_3h > 90:
        factors.append("Heavy 3-hour rainfall accumulation")
    elif rainfall_3h > 50:
        factors.append("Elevated 3-hour rainfall accumulation")

    if antecedent_rainfall > 100:
        factors.append("Very high antecedent rainfall — saturated catchment")
    elif antecedent_rainfall > 60:
        factors.append("High antecedent rainfall — reduced soil capacity")

    if soil_moisture > 0.75:
        factors.append("Critically high soil moisture — minimal infiltration capacity")
    elif soil_moisture > 0.55:
        factors.append("High soil moisture — reduced infiltration")

    if slope > 40:
        factors.append("Steep terrain — rapid surface runoff")
    elif slope > 25:
        factors.append("Moderate-to-steep slope — elevated runoff velocity")

    if land_cover == "urban":
        factors.append("Urban land cover — high impermeability")
    elif land_cover == "bare_soil":
        factors.append("Bare soil — low infiltration and high erosion risk")

    if drainage_density > 0.75:
        factors.append("High drainage density — fast channel response")

    if not factors:
        factors.append("Low environmental stress — conditions within safe range")

    return factors[:4]  # Return top 4 most relevant


def run_prediction(location_id: str, env: dict) -> dict:
    """Run ML prediction and return full result payload."""
    loc = next((l for l in LOCATIONS if l["id"] == location_id), None)
    if loc is None:
        raise HTTPException(status_code=404, detail=f"Location '{location_id}' not found.")

    land_cover  = env["land_cover"]
    lc_encoded  = le.transform([land_cover])[0]

    features = np.array([[
        env["rainfall_1h"],
        env["rainfall_3h"],
        env["rainfall_6h"],
        env["soil_moisture"],
        loc["slope"],
        loc["elevation"],
        lc_encoded,
        loc["drainage_density"],
        env["antecedent_rainfall"],
    ]])

    prob_raw      = clf.predict_proba(features)[0][1]       # probability of flood
    probability   = round(float(prob_raw) * 100, 1)
    risk_info     = classify_risk(probability)
    factors       = get_contributing_factors(
        env["rainfall_1h"], env["rainfall_3h"], env["rainfall_6h"],
        env["soil_moisture"], loc["slope"],
        env["antecedent_rainfall"], land_cover, loc["drainage_density"]
    )

    return {
        "location_id":       location_id,
        "location_name":     loc["name"],
        "flood_probability": probability,
        "risk_level":        risk_info["risk_level"],
        "color":             risk_info["color"],
        "warning":           risk_info["warning"],
        "factors":           factors,
        "conditions": {
            "rainfall_1h":         env["rainfall_1h"],
            "rainfall_3h":         env["rainfall_3h"],
            "rainfall_6h":         env["rainfall_6h"],
            "soil_moisture":       round(env["soil_moisture"] * 100, 1),
            "slope":               loc["slope"],
            "elevation":           loc["elevation"],
            "land_cover":          land_cover,
            "drainage_density":    loc["drainage_density"],
            "antecedent_rainfall": env["antecedent_rainfall"],
        },
    }


# ── Pydantic schemas ───────────────────────────────────────────────────────────

class PredictRequest(BaseModel):
    location_id:         str   = Field(..., example="valley_a")
    scenario:            str   = Field(..., example="normal")  # normal | heavy_rain | extreme_rain
    # Optional overrides — if omitted, scenario defaults are used
    rainfall_1h:         Optional[float] = None
    rainfall_3h:         Optional[float] = None
    rainfall_6h:         Optional[float] = None
    soil_moisture:       Optional[float] = None
    antecedent_rainfall: Optional[float] = None
    land_cover:          Optional[str]   = None


# ── Endpoints ──────────────────────────────────────────────────────────────────

@app.get("/api/locations")
def get_locations():
    """Return all fictional monitoring locations."""
    return {"locations": LOCATIONS}


@app.post("/api/predict")
def predict(req: PredictRequest):
    """
    Accept environmental parameters and return flood risk prediction.
    Uses scenario defaults; individual fields can override the defaults.
    """
    scenario_key = req.scenario.lower().replace(" ", "_")
    if scenario_key not in SCENARIOS:
        raise HTTPException(
            status_code=400,
            detail=f"Unknown scenario '{req.scenario}'. Valid: normal, heavy_rain, extreme_rain"
        )

    loc_scenarios = SCENARIOS[scenario_key]
    if req.location_id not in loc_scenarios:
        raise HTTPException(status_code=404, detail=f"No scenario data for location '{req.location_id}'.")

    env = dict(loc_scenarios[req.location_id])  # copy defaults

    # Apply any explicit overrides from the request
    if req.rainfall_1h         is not None: env["rainfall_1h"]         = req.rainfall_1h
    if req.rainfall_3h         is not None: env["rainfall_3h"]         = req.rainfall_3h
    if req.rainfall_6h         is not None: env["rainfall_6h"]         = req.rainfall_6h
    if req.soil_moisture       is not None: env["soil_moisture"]       = req.soil_moisture
    if req.antecedent_rainfall is not None: env["antecedent_rainfall"] = req.antecedent_rainfall
    if req.land_cover          is not None: env["land_cover"]          = req.land_cover

    return run_prediction(req.location_id, env)


@app.get("/api/predict/all")
def predict_all(scenario: str = "normal"):
    """Return predictions for every location under a given scenario."""
    scenario_key = scenario.lower().replace(" ", "_")
    if scenario_key not in SCENARIOS:
        raise HTTPException(status_code=400, detail=f"Unknown scenario '{scenario}'.")

    results = []
    for loc in LOCATIONS:
        env = dict(SCENARIOS[scenario_key].get(loc["id"], SCENARIOS["normal"][loc["id"]]))
        results.append(run_prediction(loc["id"], env))
    return {"scenario": scenario_key, "predictions": results}


@app.get("/api/summary")
def get_summary():
    """Dashboard summary statistics across all scenarios."""
    summary = {}
    for scenario_key in SCENARIOS:
        predictions = []
        for loc in LOCATIONS:
            env = dict(SCENARIOS[scenario_key][loc["id"]])
            result = run_prediction(loc["id"], env)
            predictions.append(result)

        probs      = [p["flood_probability"] for p in predictions]
        risk_counts = {"LOW": 0, "MODERATE": 0, "HIGH": 0, "SEVERE": 0}
        for p in predictions:
            risk_counts[p["risk_level"]] += 1

        summary[scenario_key] = {
            "avg_probability":  round(sum(probs) / len(probs), 1),
            "max_probability":  max(probs),
            "risk_distribution": risk_counts,
            "locations_at_risk": risk_counts["HIGH"] + risk_counts["SEVERE"],
        }

    return {
        "total_locations": len(LOCATIONS),
        "model_metrics":   MODEL_METRICS,
        "disclaimer":      "Demonstration prototype — synthetic data only.",
        "scenarios":       summary,
    }


@app.get("/api/health")
def health():
    return {"status": "ok", "model_loaded": clf is not None}


@app.get("/")
def root():
    return {
        "message": "Flash Flood Prediction API",
        "docs":    "/docs",
        "disclaimer": "Demonstration prototype — synthetic data only.",
    }
