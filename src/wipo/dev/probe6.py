import sys, pathlib; sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent / "src"))
import json
from subsets_utils import get

API = "https://api.ipstatsdc.deda.prd.web1.wipo.int/api/v1/public"
H = {"Accept": "application/json", "Accept-Language": "en"}
HC = {"Accept-Language": "en"}


def try_get(path, headers=H, label=""):
    sep = "&" if "?" in path else "?"
    try:
        r = get(f"{API}/{path}{sep}lang=en", headers=headers, timeout=(10, 120))
        body = r.text
        print(f"[{r.status_code}] {label}\n    {body[:300]}\n")
        return r
    except Exception as e:
        print(f"[ERR] {label}: {type(e).__name__} {e}\n")
        return None


# baseline (research said this failed)
try_get("pmh-search/table-result?selectedTab=pct&indicator=1001&reportType=4001&fromYear=2018&toYear=2024",
        label="table-result base 4001")
# downloadCsv
try_get("pmh-search/downloadCsv?selectedTab=pct&indicator=1001&reportType=4001&fromYear=2018&toYear=2024",
        headers=HC, label="downloadCsv base 4001")
# Try with empty selection params
try_get("pmh-search/table-result?selectedTab=pct&indicator=1001&reportType=4001&fromYear=2018&toYear=2024&pmhOffSelValues=&pmhOriSelValues=&pmhClassSelValues=",
        label="table-result + empty sel params")
# Try report type label codes differently / maybe reportType maps differently
try_get("pmh-search/table-result?selectedTab=pct&indicator=1001&reportType=4001&fromYear=1995&toYear=2026",
        label="table-result full range")
# maybe needs selectedIndicator instead of indicator
try_get("pmh-search/table-result?selectedTab=pct&selectedIndicator=1001&reportType=4001&fromYear=1995&toYear=2026",
        label="selectedIndicator param")
# maybe the chart endpoint works
try_get("pmh-search/pmhchart?selectedTab=pct&indicator=1001&reportType=4001&fromYear=1995&toYear=2026",
        label="pmhchart")
