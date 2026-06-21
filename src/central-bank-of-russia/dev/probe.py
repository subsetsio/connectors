import json
from subsets_utils import get

BASE = "https://www.cbr.ru/dataservice"


def gj(path):
    r = get(BASE + "/" + path, timeout=(10.0, 60.0))
    r.raise_for_status()
    return r.json()


# type-1 dataset with measures: pub 14 ds 25
print("=== measures ds=25 (type1) ===")
print(json.dumps(gj("measures?datasetId=25&lang=ru"), ensure_ascii=False)[:500])

print("=== years ds=25 measure=2 ===")
print(json.dumps(gj("years?datasetId=25&measureId=2&lang=ru"), ensure_ascii=False)[:400])

print("=== data ds=25 pub14 measure=2 y 2024-2025 ===")
d = gj("data?y1=2024&y2=2025&publicationId=14&datasetId=25&measureId=2&lang=ru")
print("top keys:", list(d.keys()))
print("headerData:", json.dumps(d.get("headerData"), ensure_ascii=False)[:600])
print("units:", json.dumps(d.get("units"), ensure_ascii=False)[:400])
print("RawData[0:3]:", json.dumps(d.get("RawData", [])[:3], ensure_ascii=False))
print("DTRange:", json.dumps(d.get("DTRange"), ensure_ascii=False))
print("SType:", json.dumps(d.get("SType"), ensure_ascii=False)[:300])

# type-2 dataset (no measures): pub 10 ds 17
print("\n=== measures ds=17 (type2) ===")
print(json.dumps(gj("measures?datasetId=17&lang=ru"), ensure_ascii=False)[:300])

print("=== years ds=17 measure=-1 ===")
print(json.dumps(gj("years?datasetId=17&measureId=-1&lang=ru"), ensure_ascii=False)[:400])

print("=== data ds=17 pub10 measure=-1 (full span via years) ===")
d2 = gj("data?y1=2010&y2=2026&publicationId=10&datasetId=17&measureId=-1&lang=ru")
print("headerData:", json.dumps(d2.get("headerData"), ensure_ascii=False)[:500])
print("units:", json.dumps(d2.get("units"), ensure_ascii=False)[:300])
print("RawData[0:3]:", json.dumps(d2.get("RawData", [])[:3], ensure_ascii=False))
print("n raw:", len(d2.get("RawData", [])))
