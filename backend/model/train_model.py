"""
Train a Random Forest classifier on the synthetic flood dataset.
Saves the trained model to flood_model.pkl.

NOTE: Metrics are for demonstration only — the dataset is synthetic.
"""

import os
import sys
import joblib
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE_DIR   = os.path.dirname(os.path.abspath(__file__))
DATA_PATH  = os.path.join(BASE_DIR, "..", "data", "flood_data.csv")
MODEL_PATH = os.path.join(BASE_DIR, "flood_model.pkl")

# ── Load data ──────────────────────────────────────────────────────────────────
df = pd.read_csv(DATA_PATH)
print(f"Loaded {len(df)} records from {DATA_PATH}")

# ── Encode categorical feature ─────────────────────────────────────────────────
le = LabelEncoder()
df["land_cover_enc"] = le.fit_transform(df["land_cover"])

FEATURE_COLS = [
    "rainfall_1h",
    "rainfall_3h",
    "rainfall_6h",
    "soil_moisture",
    "slope",
    "elevation",
    "land_cover_enc",
    "drainage_density",
    "antecedent_rainfall",
]
TARGET_COL = "flood_occurred"

X = df[FEATURE_COLS].values
y = df[TARGET_COL].values

# ── Train / Test split ─────────────────────────────────────────────────────────
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# ── Train model ────────────────────────────────────────────────────────────────
clf = RandomForestClassifier(
    n_estimators=100,
    max_depth=8,
    random_state=42,
    class_weight="balanced",
)
clf.fit(X_train, y_train)

# ── Evaluate ───────────────────────────────────────────────────────────────────
y_pred = clf.predict(X_test)
acc  = accuracy_score(y_test, y_pred)
prec = precision_score(y_test, y_pred, zero_division=0)
rec  = recall_score(y_test, y_pred, zero_division=0)
f1   = f1_score(y_test, y_pred, zero_division=0)

print("\n=== Model Evaluation (synthetic data — demo only) ===")
print(f"  Accuracy  : {acc:.3f}")
print(f"  Precision : {prec:.3f}")
print(f"  Recall    : {rec:.3f}")
print(f"  F1 Score  : {f1:.3f}")
print("=====================================================\n")

# ── Feature importances ────────────────────────────────────────────────────────
importances = dict(zip(FEATURE_COLS, clf.feature_importances_))
print("Feature importances:")
for feat, imp in sorted(importances.items(), key=lambda x: -x[1]):
    print(f"  {feat:<25} {imp:.4f}")

# ── Save model + encoder + metadata ───────────────────────────────────────────
payload = {
    "model":        clf,
    "label_encoder": le,
    "feature_cols": FEATURE_COLS,
    "metrics": {
        "accuracy":  round(acc, 3),
        "precision": round(prec, 3),
        "recall":    round(rec, 3),
        "f1":        round(f1, 3),
    },
}
joblib.dump(payload, MODEL_PATH)
print(f"\nModel saved to {MODEL_PATH}")
