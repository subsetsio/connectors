import httpx
from subsets_utils import get

S3 = "https://berkeley-earth-temperature.s3.us-west-1.amazonaws.com/Global/"
FILES = [
    "Land_and_Ocean_complete.txt",
    "Complete_TAVG_complete.txt",
    "Complete_TMAX_complete.txt",
    "Complete_TMIN_complete.txt",
]
for f in FILES:
    u = S3 + f
    try:
        r = get(u, timeout=(10.0, 120.0))
        lines = r.text.splitlines()
        data = [ln for ln in lines if ln.strip() and not ln.lstrip().startswith("%")]
        ncols = [len(d.split()) for d in data[:50]]
        print(f"\n==== {f} status={r.status_code} bytes={len(r.text)} datarows~{len(data)}")
        print("  field counts (first 50):", sorted(set(ncols)))
        print("  first:", repr(data[0][:140]))
        print("  last :", repr(data[-1][:140]))
    except httpx.HTTPStatusError as e:
        print(f"\n==== {f} HTTP {e.response.status_code}")
    except Exception as e:
        print(f"\n==== {f} ERR {type(e).__name__}: {e}")
