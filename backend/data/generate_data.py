"""
Synthetic flood dataset generator.
Creates realistic-looking relationships between environmental features and flood occurrence.
NOTE: This is synthetic data for demonstration purposes only.
"""

import csv
import random
import math

random.seed(42)

LAND_COVER_TYPES = ["forest", "grassland", "urban", "bare_soil", "agriculture"]

# Runoff coefficient by land cover (higher = more runoff = higher risk)
LAND_COVER_RUNOFF = {
    "forest": 0.2,
    "grassland": 0.35,
    "agriculture": 0.5,
    "bare_soil": 0.7,
    "urban": 0.85,
}

def flood_probability(rainfall_1h, rainfall_3h, rainfall_6h, soil_moisture,
                      slope, elevation, land_cover, drainage_density, antecedent_rainfall):
    """Compute a realistic flood probability score [0,1]."""
    # Normalise inputs roughly to [0,1]
    r1  = min(rainfall_1h / 100.0, 1.0)
    r3  = min(rainfall_3h / 180.0, 1.0)
    r6  = min(rainfall_6h / 250.0, 1.0)
    sm  = min(soil_moisture, 1.0)
    sl  = min(slope / 60.0, 1.0)
    ar  = min(antecedent_rainfall / 200.0, 1.0)
    dd  = min(drainage_density, 1.0)
    rc  = LAND_COVER_RUNOFF[land_cover]

    # Elevation: mid-range valleys (~800-1500 m) more vulnerable
    elev_norm = elevation / 2000.0
    elev_risk = 1.0 - abs(elev_norm - 0.55) * 1.5
    elev_risk = max(0.1, min(elev_risk, 1.0))

    score = (
        0.30 * r1 +
        0.20 * r3 +
        0.10 * r6 +
        0.15 * sm +
        0.10 * sl +
        0.05 * ar +
        0.05 * dd +
        0.03 * rc +
        0.02 * elev_risk
    )
    return min(max(score, 0.0), 1.0)


def generate_record():
    # Choose a base scenario randomly
    scenario = random.choices(
        ["dry", "normal", "wet", "heavy", "extreme"],
        weights=[15, 30, 25, 20, 10]
    )[0]

    if scenario == "dry":
        rainfall_1h         = random.uniform(0, 10)
        rainfall_3h         = random.uniform(0, 20)
        rainfall_6h         = random.uniform(0, 30)
        soil_moisture       = random.uniform(0.05, 0.30)
        antecedent_rainfall = random.uniform(0, 20)
    elif scenario == "normal":
        rainfall_1h         = random.uniform(5, 30)
        rainfall_3h         = random.uniform(15, 60)
        rainfall_6h         = random.uniform(25, 90)
        soil_moisture       = random.uniform(0.25, 0.55)
        antecedent_rainfall = random.uniform(10, 60)
    elif scenario == "wet":
        rainfall_1h         = random.uniform(20, 55)
        rainfall_3h         = random.uniform(50, 100)
        rainfall_6h         = random.uniform(80, 150)
        soil_moisture       = random.uniform(0.45, 0.70)
        antecedent_rainfall = random.uniform(40, 100)
    elif scenario == "heavy":
        rainfall_1h         = random.uniform(45, 80)
        rainfall_3h         = random.uniform(90, 150)
        rainfall_6h         = random.uniform(130, 210)
        soil_moisture       = random.uniform(0.60, 0.85)
        antecedent_rainfall = random.uniform(70, 150)
    else:  # extreme
        rainfall_1h         = random.uniform(70, 120)
        rainfall_3h         = random.uniform(130, 200)
        rainfall_6h         = random.uniform(180, 270)
        soil_moisture       = random.uniform(0.75, 0.98)
        antecedent_rainfall = random.uniform(110, 200)

    slope            = random.uniform(5, 55)
    elevation        = random.uniform(400, 2000)
    land_cover       = random.choices(
        LAND_COVER_TYPES,
        weights=[25, 20, 15, 20, 20]
    )[0]
    drainage_density = random.uniform(0.2, 1.0)

    prob = flood_probability(
        rainfall_1h, rainfall_3h, rainfall_6h,
        soil_moisture, slope, elevation,
        land_cover, drainage_density, antecedent_rainfall
    )

    # Add small noise and threshold at 0.5 for label
    noisy_prob = prob + random.gauss(0, 0.05)
    noisy_prob = max(0.0, min(1.0, noisy_prob))
    flood_occurred = 1 if noisy_prob >= 0.50 else 0

    return {
        "rainfall_1h":          round(rainfall_1h, 2),
        "rainfall_3h":          round(rainfall_3h, 2),
        "rainfall_6h":          round(rainfall_6h, 2),
        "soil_moisture":        round(soil_moisture, 3),
        "slope":                round(slope, 1),
        "elevation":            round(elevation, 0),
        "land_cover":           land_cover,
        "drainage_density":     round(drainage_density, 3),
        "antecedent_rainfall":  round(antecedent_rainfall, 2),
        "flood_occurred":       flood_occurred,
    }


FIELDS = [
    "rainfall_1h", "rainfall_3h", "rainfall_6h",
    "soil_moisture", "slope", "elevation",
    "land_cover", "drainage_density", "antecedent_rainfall",
    "flood_occurred",
]

records = [generate_record() for _ in range(250)]

import os
output_path = os.path.join(os.path.dirname(__file__), "flood_data.csv")
with open(output_path, "w", newline="") as f:
    writer = csv.DictWriter(f, fieldnames=FIELDS)
    writer.writeheader()
    writer.writerows(records)

print(f"Generated {len(records)} records.")
flood_count = sum(r["flood_occurred"] for r in records)
print(f"Flood events: {flood_count} ({flood_count/len(records)*100:.1f}%)")
print(f"No-flood events: {len(records)-flood_count}")
