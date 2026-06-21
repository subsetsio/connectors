from subsets_utils import get

BASE = "https://data.weather.gov.hk/weatherAPI/opendata/opendata.php"
ERR = "Please include valid parameters"


def probe(dataType, year, station=None):
    params = {"dataType": dataType, "rformat": "csv", "year": year}
    if station:
        params["station"] = station
    r = get(BASE, params=params, timeout=(10.0, 120.0))
    body = r.text
    valid = ERR not in body and len(body) > 200
    first = body.splitlines()[0] if body.splitlines() else ""
    print(f"{dataType} {year} st={station}: status={r.status_code} len={len(body)} valid={valid} :: {first[:60]!r}")


print("--- HHOT year boundaries (station CCH) ---")
for y in (2018, 2020, 2021, 2022, 2023, 2028, 2029, 2030, 2035):
    probe("HHOT", y, "CCH")

print("--- HLT year boundaries (station CCH) ---")
for y in (2021, 2022, 2028, 2029, 2030):
    probe("HLT", y, "CCH")

print("--- SRS year boundaries ---")
for y in (2015, 2017, 2018, 2024, 2027, 2028, 2030):
    probe("SRS", y)

print("--- MRS year boundaries + format ---")
for y in (2017, 2018, 2024, 2026, 2027, 2028):
    probe("MRS", y)

# MRS format sample
r = get(BASE, params={"dataType": "MRS", "rformat": "csv", "year": 2026}, timeout=(10.0, 120.0))
print("\nMRS 2026 sample:")
for ln in r.text.splitlines()[:6]:
    print(repr(ln))

# invalid station for HHOT
print("\n--- HHOT invalid station ---")
probe("HHOT", 2026, "ZZZ")
