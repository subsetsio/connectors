from subsets_utils import get

BASE = "https://www.ipss.go.jp/p-toukei/JMD"

# Candidate filenames per area STATS dir (HMD convention).
candidates = [
    "fltper_1x1.txt", "mltper_1x1.txt", "bltper_1x1.txt",
    "Deaths_1x1.txt", "Population.txt", "Population_1x1.txt",
    "Exposures_1x1.txt", "Mx_1x1.txt", "E0per_1x1.txt", "E0per.txt",
    "ASDR_HI.csv", "ASDR_JMDC.csv", "ASDR_HCD.csv", "ASDR_Condensed.csv",
    "ASDR.csv",
]

for area in ["00", "13"]:
    print("=" * 70)
    print("AREA", area)
    for fn in candidates:
        url = f"{BASE}/{area}/STATS/{fn}"
        try:
            r = get(url, timeout=(10.0, 60.0))
            status = r.status_code
            head = r.text[:300] if status == 200 else ""
            print(f"  {fn:22s} {status} len={len(r.text) if status==200 else 0}")
            if status == 200:
                for ln in head.splitlines()[:4]:
                    print("        |", ln)
        except Exception as e:
            print(f"  {fn:22s} ERR {type(e).__name__}: {e}")
