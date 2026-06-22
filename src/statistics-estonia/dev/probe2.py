import re, unicodedata
from subsets_utils import get, post

ROOT = "https://andmed.stat.ee/api/v1/en/stat"


def slug(s):
    if not s:
        return "col"
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    s = re.sub(r"[^0-9a-zA-Z]+", "_", s).strip("_").lower()
    return s or "col"


def ordered_codes(cat):
    idx = cat.get("index", {})
    if isinstance(idx, dict):
        return [c for c, _ in sorted(idx.items(), key=lambda kv: kv[1])]
    return list(idx)


def melt(data):
    dim_ids = data["id"]
    sizes = data["size"]
    dims = data["dimension"]
    values = data["value"]
    # column names (dedup)
    colnames, seen = [], {}
    for did in dim_ids:
        nm = slug(dims[did].get("label") or did)
        if nm in seen:
            seen[nm] += 1
            nm = f"{nm}_{seen[nm]}"
        else:
            seen[nm] = 0
        colnames.append(nm)
    codes = [ordered_codes(dims[did].get("category", {})) for did in dim_ids]
    labels = [dims[did].get("category", {}).get("label", {}) for did in dim_ids]
    rows = []
    n = len(values)
    for i in range(n):
        rem = i
        row = {}
        for d in range(len(dim_ids) - 1, -1, -1):
            pos = rem % sizes[d]
            rem //= sizes[d]
            code = codes[d][pos]
            row[colnames[d]] = labels[d].get(code, code)
        row["value"] = values[i]
        rows.append(row)
    return colnames, rows


for path in [
    "rahvastik/rahvastikunaitajad-ja-koosseis/demograafilised-pehinaitajad/RV030.PX",
    "rahvastik/rahvastikunaitajad-ja-koosseis/demograafilised-pehinaitajad/RV045.PX",
]:
    url = ROOT + "/" + path
    meta = get(url, timeout=(10, 60)).json()
    q = [{"code": v["code"], "selection": {"filter": "all", "values": ["*"]}} for v in meta["variables"]]
    data = post(url, json={"query": q, "response": {"format": "json-stat2"}}, timeout=(10, 120)).json()
    cols, rows = melt(data)
    print("===", path)
    print("title:", data.get("label"))
    print("cols:", cols, "+ value")
    print("nrows:", len(rows))
    for r in rows[:3]:
        print("  ", r)
