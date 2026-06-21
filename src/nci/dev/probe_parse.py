import csv, io, re
from subsets_utils import get

def clean_header(h):
    h = re.sub(r"\(\[[^\]]*\]\)", "", h)   # strip ([rate note])
    return h.strip().strip('"').strip()

def parse_scp(txt):
    reader = list(csv.reader(io.StringIO(txt)))
    hidx = None
    for i,row in enumerate(reader):
        if row and row[0].strip().strip('"') == "State":
            hidx = i; break
    assert hidx is not None, "no header row"
    headers = [clean_header(c) for c in reader[hidx]]
    low = [h.lower() for h in headers]
    # locate columns
    i_rate = next(i for i in range(2,len(low)) if "rate" in low[i] and "trend" not in low[i] and "rank" not in low[i])
    i_count = next((i for i in range(len(low)) if "count" in low[i]), None)
    i_dir = next((i for i in range(len(low)) if low[i]=="recent trend"), None)
    i_t5 = next((i for i in range(len(low)) if "5-year trend" in low[i]), None)
    print("headers:", headers)
    print("i_rate",i_rate,"i_count",i_count,"i_dir",i_dir,"i_t5",i_t5)
    out=[]
    for row in reader[hidx+1:]:
        if len(row) < 3: continue
        if not re.match(r"^\d{5,6}$", row[1].strip()): continue
        area = re.sub(r"\(\d+\)","", row[0]).strip().strip('"').strip()
        rec = {
            "area": area, "fips": row[1].strip(),
            "rate": row[i_rate].strip(),
            "rate_lower_ci": row[i_rate+1].strip(),
            "rate_upper_ci": row[i_rate+2].strip(),
            "avg_annual_count": row[i_count].strip() if i_count is not None else None,
            "recent_trend": row[i_dir].strip() if i_dir is not None else None,
            "recent_5yr_trend_pct": row[i_t5].strip() if i_t5 is not None else None,
        }
        out.append(rec)
    return out

for path,typ,extra in [("incidencerates","incd",{"stage":"999"}),("deathrates","death",{})]:
    p=dict(stateFIPS="00",areatype="state",cancer="001",race="00",sex="0",age="001",year="0",type=typ,sortVariableName="rate",sortOrder="desc",output="1"); p.update(extra)
    r=get("https://statecancerprofiles.cancer.gov/%s/index.php"%path, params=p, timeout=(10,120)); r.raise_for_status()
    rows=parse_scp(r.text)
    print(f"\n== {path}: {len(rows)} data rows ==")
    for rec in rows[:4]: print(rec)
