"""Quick API smoke tests."""
import urllib.request
import json

BASE = "http://localhost:8000"

def post(path, data):
    body = json.dumps(data).encode()
    req = urllib.request.Request(
        BASE + path, data=body,
        headers={"Content-Type": "application/json"}, method="POST"
    )
    with urllib.request.urlopen(req) as r:
        return json.loads(r.read())

def get(path):
    with urllib.request.urlopen(BASE + path) as r:
        return json.loads(r.read())

print("=== All locations across all scenarios ===")
for scenario in ["normal", "heavy_rain", "extreme_rain"]:
    all_r = get(f"/api/predict/all?scenario={scenario}")
    print(f"\n--- {scenario.upper()} ---")
    for p in all_r["predictions"]:
        print(f"  {p['location_name']:<20} {p['flood_probability']:>6.1f}%  {p['risk_level']}")
