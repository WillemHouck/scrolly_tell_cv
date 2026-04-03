import xml.etree.ElementTree as ET
import json
import math

tree = ET.parse(
    "/Users/willemhouck/Documents/vs_code/scrolly_tell_cv/wildstrubel/Ploeteren_door_de_alpen_Wildstrubel.gpx"
)
ns = {"g": "http://www.topografix.com/GPX/1/1"}

pts = tree.findall(".//g:trkpt", ns)
raw = []
for p in pts:
    ele_el = p.find("g:ele", ns)
    ele = float(ele_el.text) if ele_el is not None and ele_el.text else None
    if ele and ele > 0:
        raw.append({"lat": float(p.get("lat")), "lon": float(p.get("lon")), "ele": ele})


def haversine(p1, p2):
    R = 6371000
    dlat = math.radians(p2["lat"] - p1["lat"])
    dlon = math.radians(p2["lon"] - p1["lon"])
    a = (
        math.sin(dlat / 2) ** 2
        + math.cos(math.radians(p1["lat"]))
        * math.cos(math.radians(p2["lat"]))
        * math.sin(dlon / 2) ** 2
    )
    return R * 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))


total_dist = 0
for i in range(1, len(raw)):
    total_dist += haversine(raw[i - 1], raw[i])

TARGET = 300
step_dist = total_dist / TARGET

sampled = [raw[0]]
accum = 0
for i in range(1, len(raw)):
    accum += haversine(raw[i - 1], raw[i])
    if accum >= step_dist:
        sampled.append(raw[i])
        accum = 0
sampled.append(raw[-1])

print(f"Total distance: {total_dist/1000:.1f} km")
print(f"Sampled points: {len(sampled)}")

with open(
    "/Users/willemhouck/Documents/vs_code/scrolly_tell_cv/wildstrubel/trail_data.json",
    "w",
) as f:
    json.dump(sampled, f)

print("Written to trail_data.json")
