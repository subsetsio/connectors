"""Probe TIC parsers against live files."""
import csv as stdlib_csv
import io
from datetime import datetime
from subsets_utils import get

MONTH_MAP = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
             "Jul":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
SKIP_PREFIXES = ("Grand Total", "Of Which", "Of which")


def _val(s):
    s = (s or "").strip()
    if not s or s in ("------", "n/a", "N/A", "--", "(*)"):
        return None
    try:
        return float(s.replace(",", ""))
    except ValueError:
        return None


def _is_summary(country):
    c = country.strip()
    return (not c) or c.startswith("-") or any(c.startswith(p) for p in SKIP_PREFIXES)


def parse_slt(text):
    lines = list(stdlib_csv.reader(io.StringIO(text), delimiter="\t"))
    hdr_idx = None
    for i, line in enumerate(lines):
        if line and line[0].strip() == "country":
            hdr_idx = i
            break
    assert hdr_idx is not None, "no machine header"
    cols = [c.strip() for c in lines[hdr_idx] if c.strip()]
    rows = []
    for line in lines[hdr_idx + 1:]:
        if not line or not line[0].strip():
            break
        rec = {}
        for j, col in enumerate(cols):
            cell = line[j] if j < len(line) else ""
            if j < 3:
                rec[col] = cell.strip()
            else:
                rec[col] = _val(cell)
        rows.append(rec)
    return cols, rows


def parse_mfh_wide(text):
    """slt_table5 current: header row 'Country' then YYYY-MM date columns."""
    lines = list(stdlib_csv.reader(io.StringIO(text), delimiter="\t"))
    hidx = None
    for i, line in enumerate(lines):
        if line and line[0].strip() == "Country":
            hidx = i
            break
    assert hidx is not None
    dates = [c.strip() for c in lines[hidx]]
    out = {}
    for line in lines[hidx + 1:]:
        if not line or not line[0].strip():
            continue
        country = line[0].strip()
        if _is_summary(country):
            continue
        for ci in range(1, min(len(line), len(dates))):
            d = dates[ci]
            if not d:
                continue
            v = _val(line[ci])
            if v is not None:
                out[(country, d)] = v
    return out


def parse_mfh_hist(text):
    lines = list(stdlib_csv.reader(io.StringIO(text), delimiter="\t"))
    out = {}
    i = 0
    while i < len(lines):
        line = lines[i]
        if not line or line[0].strip() != "Country":
            i += 1
            continue
        year_row = line
        month_row = lines[i - 1] if i > 0 else []
        dates = []
        for ci in range(len(year_row)):
            month = month_row[ci].strip() if ci < len(month_row) else ""
            year = year_row[ci].strip()
            if month in MONTH_MAP and year.isdigit():
                dates.append((ci, f"{year}-{MONTH_MAP[month]}"))
        i += 1
        if i < len(lines) and lines[i] and any("---" in c for c in lines[i]):
            i += 1
        while i < len(lines):
            dl = lines[i]
            if not dl or not dl[0].strip():
                break
            country = dl[0].strip()
            if _is_summary(country):
                i += 1
                continue
            for ci, d in dates:
                if ci < len(dl):
                    v = _val(dl[ci])
                    if v is not None:
                        out[(country, d)] = v
            i += 1
        i += 1
    return out


def parse_fht(text):
    out = {}
    for line in stdlib_csv.reader(io.StringIO(text)):
        if len(line) < 2 or not line[0].strip():
            continue
        raw = line[0].strip()
        if raw.startswith("-") or raw == "Date":
            continue
        try:
            dt = datetime.strptime(raw, "%d-%b-%Y")
        except ValueError:
            continue
        v = _val(line[1])
        if v is not None:
            out[("Total Foreign Holdings", dt.strftime("%Y-%m"))] = v
    return out


BASE_RC = "https://ticdata.treasury.gov/resource-center/data-chart-center/tic/Documents"
BASE_PUB = "https://ticdata.treasury.gov/Publish"

for n in (1, 2, 3, 4):
    t = get(f"{BASE_RC}/slt_table{n}.txt", timeout=(10, 120)).text
    cols, rows = parse_slt(t)
    dates = sorted({r["date"] for r in rows})
    print(f"slt_table{n}: {len(cols)} cols, {len(rows)} rows, dates {dates[0]}..{dates[-1]}, countries {len({r['country'] for r in rows})}")
    print(f"   cols: {cols}")
    print(f"   sample: {rows[0]}")

cur = parse_mfh_wide(get(f"{BASE_RC}/slt_table5.txt", timeout=(10, 120)).text)
hist = parse_mfh_hist(get(f"{BASE_PUB}/mfhhis01.txt", timeout=(10, 120)).text)
agg = parse_fht(get(f"{BASE_PUB}/fht_1939-1999.csv", timeout=(10, 120)).text)
print(f"\nMFH current={len(cur)} hist={len(hist)} agg={len(agg)}")
merged = {}
merged.update(agg); merged.update(hist); merged.update(cur)
ds = sorted({d for _, d in merged})
print(f"MFH merged={len(merged)} dates {ds[0]}..{ds[-1]} countries {len({c for c,_ in merged})}")
print("sample countries:", sorted({c for c, _ in merged})[:8])
