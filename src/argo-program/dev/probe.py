from subsets_utils import get

BASE = "https://erddap.ifremer.fr/erddap/tabledap"

def size(url, label):
    try:
        r = get(url, timeout=(10.0, 180.0))
        n = r.text.count("\n")
        print(f"{label}: HTTP {r.status_code}, {len(r.content)} bytes, ~{n} lines")
        # print first 3 lines
        for line in r.text.splitlines()[:3]:
            print("   ", line[:200])
    except Exception as e:
        print(f"{label}: ERROR {type(e).__name__}: {str(e)[:300]}")

# 1. ArgoFloats: one day, minimal columns -> how many measurement rows per day?
size(f"{BASE}/ArgoFloats.csv?platform_number,time,pres&time%3E=2024-06-01T00:00:00Z&time%3C=2024-06-02T00:00:00Z",
     "ArgoFloats 1 day (2024-06-01)")

# 2. ArgoFloats: one full month -> volume + does ERDDAP cap it?
size(f"{BASE}/ArgoFloats.csv?platform_number,time,pres&time%3E=2024-06-01T00:00:00Z&time%3C=2024-07-01T00:00:00Z",
     "ArgoFloats 1 month (2024-06)")

# 3. Index: full dataset row count + size (one column)
size(f"{BASE}/ArgoFloats-index.csv?file", "ArgoFloats-index full (file col only)")

# 4. reference: full
size(f"{BASE}/ArgoFloats-reference.csv?platform_number,time,pres,temp,psal&time%3E=2024-01-01T00:00:00Z&time%3C=2024-02-01T00:00:00Z",
     "ArgoFloats-reference 1 month")

# 5. OACP-Argo-Global full
size(f"{BASE}/OACP-Argo-Global.csv?longitude,latitude,PPD", "OACP-Argo-Global (3 cols)")

# 6. BGC one month
size(f"{BASE}/ArgoFloats-synthetic-BGC.csv?platform_number,time,pres,doxy&time%3E=2024-06-01T00:00:00Z&time%3C=2024-07-01T00:00:00Z",
     "BGC 1 month (2024-06)")
