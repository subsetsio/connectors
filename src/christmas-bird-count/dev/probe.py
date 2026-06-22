import csv, io, re
from subsets_utils import get

BASE = "https://netapp.audubon.org/CBCObservation/Reports/HistoricalResultsByCount.aspx"

def fetch(cid, sy=1, ey=140):
    r = get(BASE, params={"rf": "CSV", "cid": cid, "sy": sy, "ey": ey}, timeout=(10,120))
    r.raise_for_status()
    return r.text

def parse(text):
    rows = list(csv.reader(io.StringIO(text)))
    circle = None
    obs = []
    section = None
    for r in rows:
        if not r or not r[0].strip():
            continue
        head = r[0].strip()
        if head == "CircleName":
            section = "circle_hdr"; continue
        if head == "COM_NAME":
            section = "obs"; continue
        if head.startswith("CountYear"):  # weather/effort sub-tables — skip
            section = "skip"; continue
        if head.startswith("#"):
            continue
        if section == "circle_hdr" and circle is None:
            latlong = r[2] if len(r) > 2 else ""
            lat = lon = None
            if "/" in latlong:
                a, b = latlong.split("/", 1)
                try: lat, lon = float(a), float(b)
                except ValueError: pass
            circle = {"name": r[0], "abbrev": r[1] if len(r)>1 else None, "lat": lat, "lon": lon}
            section = None
        elif section == "obs" and len(r) >= 5:
            com = r[0]; cyear = r[1]; how = r[2].strip(); npph = r[3].strip(); flags = r[4].strip()
            if not how:  # species not reported this year
                continue
            parts = com.split("\n")
            common = parts[0].strip()
            sci = None
            for p in parts[1:]:
                p = p.strip()
                if p.startswith("[") and p.endswith("]"): sci = p[1:-1]
            cy_lines = cyear.split("\n")
            m = re.match(r"\s*(\d{4})\s*\[(\d+)\]", cy_lines[0])
            season_year = int(m.group(1)) if m else None
            count_year = int(m.group(2)) if m else None
            count_date = None
            for ln in cy_lines:
                mm = re.search(r"Count Date:\s*([\d/]+)", ln)
                if mm: count_date = mm.group(1)
            cw = (how.lower() == "cw")
            how_many = None if cw or not how.isdigit() else int(how)
            try: npph_v = float(npph) if npph else None
            except ValueError: npph_v = None
            obs.append({"common": common, "sci": sci, "count_year": count_year,
                        "season_year": season_year, "count_date": count_date,
                        "how_many": how_many, "cw": cw, "npph": npph_v, "flags": flags or None})
    return circle, obs

for cid in (56980, 60000):
    t = fetch(cid)
    c, obs = parse(t)
    print(f"\ncid={cid} bytes={len(t)} circle={c} n_obs={len(obs)}")
    for o in obs[:3]: print("  ", o)
    yrs = sorted({o['season_year'] for o in obs if o['season_year']})
    print("  year span:", (yrs[0], yrs[-1]) if yrs else None, " distinct species:", len({o['common'] for o in obs}))
    print("  cw count:", sum(1 for o in obs if o['cw']), " how_many nulls:", sum(1 for o in obs if o['how_many'] is None))
