# AI-Powered Flash Flood Prediction System
**Hilly Region Early Warning System — Demonstration Prototype**

> ⚠ **This is a demonstration prototype using entirely synthetic data.**
> It does not use real-time IMD data, satellite imagery, radar data, or any
> operational government forecast. All predictions are illustrative only.

---

## Features

- Interactive Leaflet map with colour-coded risk markers (green → red)
- Three scenario modes: Normal / Heavy Rain / Extreme Rain
- Random Forest ML model predicting flood probability per location
- Risk classification: LOW / MODERATE / HIGH / SEVERE
- Automatic warning modal for HIGH and SEVERE risk
- "Why is this location at risk?" explainability panel
- Environmental conditions display (rainfall, soil moisture, slope, elevation)
- System status indicator (Data / Model / Prediction)
- AI pipeline visualisation at the bottom of the dashboard
- Fully responsive — desktop, laptop, tablet

---

## Architecture

```
┌─────────────────────────────────────────────────────────┐
│  React Frontend (Vite, React-Leaflet)  :5173            │
│  ┌──────────┐  ┌──────────┐  ┌──────────────────────┐  │
│  │ Scenario │  │ Risk Card│  │   Leaflet Map         │  │
│  │ Selector │  │ + Gauge  │  │   (7 locations)       │  │
│  └──────────┘  └──────────┘  └──────────────────────┘  │
│  ┌──────────────────────────────────────────────────┐   │
│  │  Conditions Panel  +  "Why at risk?" Factors     │   │
│  └──────────────────────────────────────────────────┘   │
└───────────────────────┬─────────────────────────────────┘
                 Vite proxy /api → :8000
┌──────────────────────────────────────────────────────────┐
│  FastAPI Backend  :8000                                  │
│  /api/locations   /api/predict   /api/predict/all        │
│  /api/summary     /api/health                            │
└───────────────────────┬──────────────────────────────────┘
                        │
┌───────────────────────▼──────────────────────────────────┐
│  scikit-learn Random Forest                              │
│  Trained on 250 synthetic records                        │
│  flood_model.pkl                                         │
└──────────────────────────────────────────────────────────┘
```

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18, Vite 5, React-Leaflet 4, Axios |
| Backend | Python 3.9+, FastAPI, Uvicorn |
| Machine Learning | scikit-learn (Random Forest), pandas, numpy, joblib |
| Map | Leaflet.js via React-Leaflet, OpenStreetMap tiles |
| Data | Synthetic CSV (250 records, generated locally) |

---

## Synthetic Data Explanation

The dataset (`backend/data/flood_data.csv`) was generated programmatically with
realistic feature relationships:

- Higher rainfall → higher flood score
- Higher soil moisture → reduced infiltration → higher risk
- Steeper slope → faster runoff → higher risk
- Urban / bare-soil land cover → less absorption → higher risk
- High antecedent rainfall → pre-saturated soil → higher risk

**This data is fictional.** It exists only to train and demonstrate the software
pipeline. No claims are made about real-world accuracy.

---

## Machine Learning Model

| Property | Value |
|----------|-------|
| Algorithm | Random Forest Classifier |
| Trees | 100 |
| Max depth | 8 |
| Training records | 188 (75% of 250) |
| Test records | 62 (25% of 250) |
| Class weighting | Balanced |

**Evaluation on synthetic test set (demo only):**

| Metric | Value |
|--------|-------|
| Accuracy | 0.905 |
| Precision | 0.864 |
| Recall | 0.864 |
| F1 Score | 0.864 |

Features used: `rainfall_1h`, `rainfall_3h`, `rainfall_6h`, `soil_moisture`,
`slope`, `elevation`, `land_cover`, `drainage_density`, `antecedent_rainfall`

---

## Risk Classification

| Probability | Level | Map Colour |
|-------------|-------|-----------|
| 0 – 30% | LOW | 🟢 Green |
| 30 – 60% | MODERATE | 🟡 Yellow |
| 60 – 80% | HIGH | 🟠 Orange |
| 80 – 100% | SEVERE | 🔴 Red |

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/health` | Server health check |
| GET | `/api/locations` | All 7 monitoring locations |
| POST | `/api/predict` | Predict for one location + scenario |
| GET | `/api/predict/all?scenario=` | Predict for all locations |
| GET | `/api/summary` | Scenario statistics + model metrics |

### POST /api/predict — example

Request:
```json
{ "location_id": "valley_a", "scenario": "extreme_rain" }
```

Response:
```json
{
  "location_name": "Valley A",
  "flood_probability": 100.0,
  "risk_level": "SEVERE",
  "warning": "SEVERE flash flood risk. Immediate preparedness is required.",
  "factors": [
    "Very high 1-hour rainfall intensity",
    "Heavy 3-hour rainfall accumulation",
    "Very high antecedent rainfall — saturated catchment",
    "Critically high soil moisture — minimal infiltration capacity"
  ]
}
```

Valid `scenario` values: `normal` · `heavy_rain` · `extreme_rain`

---

## Prerequisites

| Tool | Min version | Check |
|------|------------|-------|
| Python | 3.9 | `python --version` |
| Node.js | 18 | `node --version` |
| npm | 8 | `npm --version` |

---

## How to Run

Open **two terminals**.

### Terminal 1 — Backend

```bash
cd flood-prediction/backend

# Install dependencies (first time only)
pip install fastapi uvicorn scikit-learn pandas numpy joblib python-multipart

# (Optional) Regenerate the dataset
python data/generate_data.py

# (Optional) Retrain the model
python model/train_model.py

# Start the API server
python -m uvicorn main:app --reload --port 8000
```

API available at: **http://localhost:8000**
Interactive API docs: **http://localhost:8000/docs**

---

### Terminal 2 — Frontend

```bash
cd flood-prediction/frontend

# Install dependencies (first time only)
npm install

# Start the development server
npm run dev
```

Dashboard available at: **http://localhost:5173**

---

## Demo Sequence (60–90 seconds)

Follow these steps to demonstrate the full system:

1. Open **http://localhost:5173**
2. The map loads showing 7 fictional hilly-region locations — all markers are **green** (LOW)
3. The sidebar shows **Valley A** selected under the **Normal** scenario
4. The Risk Card shows **0% — LOW**
5. The Environmental Conditions panel shows low rainfall and soil moisture values
6. **Click "Heavy Rain"** scenario button
   - Valley A updates to **~52% — MODERATE**
   - Map markers shift to yellow/orange depending on location
   - Status panel shows "Updated HH:MM:SS"
7. **Click "Extreme Rain"** scenario button
   - Valley A jumps to **100% — SEVERE**
   - All map markers turn **red**
   - Warning modal appears automatically with recommended actions
   - Click **Acknowledge** to dismiss
8. Scroll down the sidebar to see **"Why is this location at risk?"**
   - Shows ✓ checkmark factors: high rainfall, saturated soil, etc.
9. **Click a different location** on the map (e.g. River Zone D)
   - Sidebar updates instantly to that location's conditions
10. Point to the **System Pipeline** bar at the bottom:
    `Data → Processing → AI Model → Risk → Warning`

---

## Project Structure

```
flood-prediction/
│
├── backend/
│   ├── main.py                    ← FastAPI app — all endpoints + prediction logic
│   ├── requirements.txt
│   ├── test_api.py                ← API smoke tests
│   ├── test_full_flow.py          ← End-to-end test
│   ├── model/
│   │   ├── train_model.py         ← Random Forest training script
│   │   └── flood_model.pkl        ← Saved trained model
│   └── data/
│       ├── flood_data.csv         ← Synthetic dataset (250 records)
│       └── generate_data.py       ← Dataset generation script
│
├── frontend/
│   ├── index.html
│   ├── vite.config.js             ← Vite + /api proxy config
│   ├── package.json
│   └── src/
│       ├── App.jsx                ← Root component + state management
│       ├── main.jsx
│       ├── index.css              ← All styles
│       ├── services/
│       │   └── api.js             ← Axios API layer (relative URLs)
│       └── components/
│           ├── Header.jsx
│           ├── ScenarioSelector.jsx
│           ├── FloodMap.jsx       ← React-Leaflet map
│           ├── RiskCard.jsx       ← Probability gauge + risk badge
│           ├── ConditionsPanel.jsx ← Env data + "Why at risk?" factors
│           ├── StatusPanel.jsx    ← System status indicators
│           ├── WarningModal.jsx   ← Auto-shown for HIGH/SEVERE
│           └── SystemFlow.jsx     ← AI pipeline visualisation
│
└── README.md
```

---

## Troubleshooting

**"Cannot reach backend" error in the dashboard**
Make sure the backend is running on port 8000 before opening the frontend.

**`ModuleNotFoundError` on backend start**
```bash
pip install fastapi uvicorn scikit-learn pandas numpy joblib python-multipart
```

**`FileNotFoundError: flood_model.pkl`**
```bash
python flood-prediction/backend/model/train_model.py
```

**Map tiles not loading**
The map uses OpenStreetMap — an internet connection is required for tile imagery.
All prediction functionality works fully offline.

---

## Future Improvements

| Current (Demo) | Real-world Replacement |
|----------------|----------------------|
| Synthetic CSV dataset | IMD / satellite / radar rainfall feeds |
| Hardcoded scenario presets | Live sensor polling + weather API |
| Static location coordinates | GPS / IoT sensor network |
| Manual model reload | Scheduled retraining pipeline |
| Simulated warning modal | SMS / push notification / sirens |
| OpenStreetMap tiles | High-resolution terrain tiles |
| Single-node FastAPI | Scalable microservices + message queue |

---

*Demonstration Prototype — Synthetic Data Only — Not an operational forecast system*
