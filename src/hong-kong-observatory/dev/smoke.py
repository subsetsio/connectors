import pyarrow as pa
import nodes.hong_kong_observatory as m

# RYES parse on one day
payload = m._fetch_json({"dataType": "RYES", "rformat": "json", "date": "20260615", "lang": "en"})
rows = m._parse_ryes_day(payload, "20260615")
print("RYES rows:", len(rows), "sample:", rows[:3])
print("RYES metrics:", sorted({r['metric'] for r in rows}))
print("RYES stations:", sorted({r['station'] for r in rows})[:6], "...")
pa.Table.from_pylist(rows, schema=m._RYES_SCHEMA)  # schema check

# HLT parse on one station/year
txt = m._fetch_text({"dataType": "HLT", "rformat": "csv", "station": "CCH", "year": 2026})
cr = m._csv_rows(txt)
sample = []
for r in cr[1:4]:
    month, day = int(r[0]), int(r[1])
    pairs = r[2:]
    for idx in range(0, len(pairs) - 1, 2):
        t, h = pairs[idx].strip(), pairs[idx+1].strip()
        if t == "" and h == "":
            continue
        sample.append({"station":"CCH","year":2026,"month":month,"day":day,"event":idx//2+1,"time":t,"height_m":h})
print("\nHLT sample:", sample[:5])
pa.Table.from_pylist(sample, schema=m._HLT_SCHEMA)

# HHOT one station/year - count
txt = m._fetch_text({"dataType": "HHOT", "rformat": "csv", "station": "CCH", "year": 2026})
cr = m._csv_rows(txt)
print("\nHHOT header:", cr[0][:5], "data rows:", len(cr)-1)

# discover years
print("\nHHOT years:", m._discover_years("HHOT", "CCH"))
print("SRS years:", m._discover_years("SRS"))

# CLM one station parse count
txt = m._fetch_text({"dataType": "CLMTEMP", "rformat": "csv", "station": "HKO"})
cr = m._csv_rows(txt)
n = sum(1 for r in cr if len(r) >= 4 and r[0].isdigit() and len(r[0]) == 4)
print("\nCLMTEMP HKO data rows:", n, "first:", cr[3], "last-data check")
print("OK")
