"""
Final end-to-end smoke test.
Run from the project root: python flood-prediction/backend/test_full_flow.py
"""
import urllib.request
import json

BASE_F = "http://localhost:5173"
BASE_B = "http://localhost:8000"

PASS = "✓"
FAIL = "✗"

errors = []

def get(url):
    with urllib.request.urlopen(url, timeout=8) as r:
        return json.loads(r.read())

def post(url, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(url, data=body,
                                  headers={"Content-Type": "application/json"},
                                  method="POST")
    with urllib.request.urlopen(req, timeout=8) as r:
        return json.loads(r.read())

def check(label, condition, detail=""):
    if condition:
        print(f"  {PASS} {label}")
    else:
        print(f"  {FAIL} {label}  ← {detail}")
        errors.append(label)

print("\n=== Flash Flood System — Final Demo Test ===\n")

# ── 1. Services reachable ──────────────────────────────────────────
print("[ Services ]")
try:
    with urllib.request.urlopen(BASE_F, timeout=5) as r:
        html = r.read().decode()
    check("Frontend serves HTML", "root" in html)
except Exception as e:
    check("Frontend serves HTML", False, str(e))

try:
    h = get(f"{BASE_B}/api/health")
    check("Backend health OK", h.get("status") == "ok")
    check("Model loaded", h.get("model_loaded") is True)
except Exception as e:
    check("Backend health OK", False, str(e))

# ── 2. Locations ───────────────────────────────────────────────────
print("\n[ Locations ]")
try:
    locs = get(f"{BASE_B}/api/locations")["locations"]
    check("Returns 7 locations", len(locs) == 7)
    ids = {l["id"] for l in locs}
    check("valley_a present", "valley_a" in ids)
    check("All have lat/lng", all("lat" in l and "lng" in l for l in locs))
except Exception as e:
    check("Locations endpoint", False, str(e))

# ── 3. Demo sequence — Valley A across all 3 scenarios ────────────
print("\n[ Demo Sequence — Valley A ]")
EXPECTED = {
    "normal":       ("LOW",      lambda p: p < 30),
    "heavy_rain":   ("MODERATE or HIGH", lambda p: 30 <= p < 80),
    "extreme_rain": ("SEVERE",   lambda p: p >= 80),
}
for sc, (expected_label, prob_check) in EXPECTED.items():
    try:
        r = post(f"{BASE_B}/api/predict", {"location_id": "valley_a", "scenario": sc})
        prob = r["flood_probability"]
        level = r["risk_level"]
        check(
            f"{sc:<15} → {prob:>5.1f}%  {level:<10} (expected {expected_label})",
            prob_check(prob),
            f"got {prob}% {level}"
        )
        if sc != "normal":
            check(f"  Warning present for {sc}", bool(r.get("warning")))
            check(f"  Factors present for {sc}", len(r.get("factors", [])) >= 1)
    except Exception as e:
        check(f"{sc} prediction", False, str(e))

# ── 4. Map markers — predict/all ──────────────────────────────────
print("\n[ Map Markers ]")
for sc in ["normal", "extreme_rain"]:
    try:
        preds = get(f"{BASE_B}/api/predict/all?scenario={sc}")["predictions"]
        check(f"predict/all returns 7 for {sc}", len(preds) == 7)
        if sc == "normal":
            all_low = all(p["risk_level"] == "LOW" for p in preds)
            check("Normal → all LOW", all_low)
        else:
            all_sev = all(p["risk_level"] == "SEVERE" for p in preds)
            check("Extreme → all SEVERE", all_sev)
    except Exception as e:
        check(f"predict/all {sc}", False, str(e))

# ── 5. Heavy rain spread ───────────────────────────────────────────
print("\n[ Heavy Rain Spread ]")
try:
    preds = get(f"{BASE_B}/api/predict/all?scenario=heavy_rain")["predictions"]
    levels = {p["risk_level"] for p in preds}
    has_spread = len(levels) >= 2
    check("Multiple risk levels in heavy_rain", has_spread, f"got {levels}")
    no_low_only = "MODERATE" in levels or "HIGH" in levels or "SEVERE" in levels
    check("At least MODERATE or above", no_low_only)
    for p in preds:
        print(f"    {p['location_name']:<22} {p['flood_probability']:>5.1f}%  {p['risk_level']}")
except Exception as e:
    check("Heavy rain spread", False, str(e))

# ── 6. Summary endpoint ────────────────────────────────────────────
print("\n[ Summary ]")
try:
    s = get(f"{BASE_B}/api/summary")
    check("Total locations = 7", s["total_locations"] == 7)
    check("Model metrics present", "accuracy" in s.get("model_metrics", {}))
    check("Disclaimer present", "synthetic" in s.get("disclaimer", "").lower())
    check("All 3 scenarios in summary", set(s["scenarios"].keys()) == {"normal", "heavy_rain", "extreme_rain"})
except Exception as e:
    check("Summary endpoint", False, str(e))

# ── Result ─────────────────────────────────────────────────────────
print("\n" + "=" * 44)
if not errors:
    print(f"  {PASS} ALL CHECKS PASSED — system is demo-ready")
else:
    print(f"  {FAIL} {len(errors)} check(s) failed:")
    for e in errors:
        print(f"      • {e}")
print("=" * 44 + "\n")
