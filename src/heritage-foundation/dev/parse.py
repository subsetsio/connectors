import io, re
import pandas as pd
from subsets_utils import get

AZURE = "https://indexdotnet.azurewebsites.net/index/excel/{y}/index{y}_data.xls"
STATIC = "https://static.heritage.org/index/data/{y}/{y}_indexofeconomicfreedom_data.xlsx"

def norm(s):
    return re.sub(r"[^a-z0-9]+", " ", str(s).lower()).strip()

def classify(h):
    n = norm(h)
    if not n or n == "nan": return None
    if "change" in n: return None
    if n in ("countryid","webname","web name","world rank","region rank","year","id","country id"): return None
    if n in ("country","country name"): return "__country__"
    if n == "region": return "__region__"
    # overall
    if "overall" in n or re.search(r"\b\d{4}\b score", n) or n.endswith(" score") or n == "score": return "overall"
    if "property" in n: return "property_rights"
    if "judic" in n: return "judicial_effectiveness"
    if "integrity" in n: return "government_integrity"
    if "corruption" in n: return "freedom_from_corruption"
    if "tax" in n: return "tax_burden"
    if "fiscal health" in n: return "fiscal_health"
    if "fiscal" in n: return "fiscal_freedom"
    if "spending" in n: return "government_spending"
    if "gov" in n and "size" in n: return "government_size"
    if "business" in n: return "business_freedom"
    if "labor" in n or "labour" in n: return "labor_freedom"
    if "monetary" in n or "monitary" in n or "monet" in n: return "monetary_freedom"
    if "trade" in n: return "trade_freedom"
    if "investment" in n or "invest" in n: return "investment_freedom"
    if "financial" in n or "financ" in n: return "financial_freedom"
    return None

def to_score(v):
    if v is None: return None
    s = str(v).strip().replace(",", "")
    if s in ("", "-", "nan", "N/A", "NA", "n/a", "None"): return None
    try: return float(s)
    except ValueError: return None

def parse(year, content, engine):
    raw = pd.read_excel(io.BytesIO(content), sheet_name=0, header=None, engine=engine)
    # find header row
    hidx = None
    for i in range(min(5, len(raw))):
        c0 = norm(raw.iloc[i, 0])
        if c0.startswith("country"):
            hidx = i; break
    if hidx is None: raise RuntimeError(f"{year}: no header row")
    headers = raw.iloc[hidx].tolist()
    colmap = {}
    country_col = region_col = None
    for j, h in enumerate(headers):
        c = classify(h)
        if c == "__country__":
            # prefer 'country name' over 'country'
            if country_col is None or norm(h) == "country name":
                country_col = j
        elif c == "__region__":
            region_col = j
        elif c:
            colmap.setdefault(c, j)  # first wins
    rows = []
    for r in range(hidx+1, len(raw)):
        country = raw.iloc[r, country_col]
        if pd.isna(country) or not str(country).strip(): continue
        country = str(country).strip()
        region = None
        if region_col is not None:
            rv = raw.iloc[r, region_col]
            region = None if pd.isna(rv) else str(rv).strip() or None
        for comp, j in colmap.items():
            sc = to_score(raw.iloc[r, j])
            rows.append((year, country, region, comp, sc))
    return rows, sorted(colmap.keys()), country_col, region_col

for y, tmpl, eng in [(2009,AZURE,"xlrd"),(2013,AZURE,"xlrd"),(2024,STATIC,"openpyxl"),(2026,STATIC,"openpyxl")]:
    r = get(tmpl.format(y=y), timeout=(10,120))
    rows, comps, cc, rc = parse(y, r.content, eng)
    nonnull = sum(1 for x in rows if x[4] is not None)
    print(f"{y}: rows={len(rows)} nonnull={nonnull} country_col={cc} region_col={rc}")
    print(f"   components: {comps}")
    print(f"   sample: {rows[20] if len(rows)>20 else rows[:2]}")
