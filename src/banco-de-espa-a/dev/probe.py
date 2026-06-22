import csv
import io
import re
import zipfile
from subsets_utils import get

MONTHS = {"ENE":1,"FEB":2,"MAR":3,"ABR":4,"MAY":5,"JUN":6,
          "JUL":7,"AGO":8,"SEP":9,"OCT":10,"NOV":11,"DIC":12}
RE_DAILY = re.compile(r"^(\d{1,2})\s+([A-Z]{3})\.?\s*(\d{4})$")
RE_MONTH = re.compile(r"^([A-Z]{3})\.?\s*(\d{4})$")
RE_YEAR  = re.compile(r"^(\d{4})$")

def parse_period(label):
    label = label.strip().upper()
    m = RE_DAILY.match(label)
    if m:
        d, mon, y = m.groups()
        if mon in MONTHS:
            return f"{int(y):04d}-{MONTHS[mon]:02d}-{int(d):02d}"
    m = RE_MONTH.match(label)
    if m:
        mon, y = m.groups()
        if mon in MONTHS:
            return f"{int(y):04d}-{MONTHS[mon]:02d}-01"
    m = RE_YEAR.match(label)
    if m:
        return f"{int(m.group(1)):04d}-01-01"
    return None

def parse_value(raw):
    raw = raw.strip()
    if raw in ("", "_"):
        return None
    try:
        return float(raw)
    except ValueError:
        try:
            return float(raw.replace(",", "."))
        except ValueError:
            return None

def parse_csv(text):
    rows = list(csv.reader(io.StringIO(text)))
    codes = rows[0][1:]
    freq_row = None
    for r in rows[:8]:
        if r and r[0].strip().upper().startswith("FRECUENCIA"):
            freq_row = r[1:]
    out = []
    skipped_labels = set()
    for r in rows[6:]:
        if not r:
            continue
        label = r[0].strip()
        date = parse_period(label)
        if date is None:
            skipped_labels.add(label[:20])
            continue
        for i, code in enumerate(codes):
            val = parse_value(r[i+1]) if i+1 < len(r) else None
            if val is None:
                continue
            freq = freq_row[i] if freq_row and i < len(freq_row) else None
            out.append((code, date, val, freq, label))
    return out, skipped_labels

# probe ti.zip (daily) and be.zip one quarterly file
for zid in ["ti", "be"]:
    resp = get(f"https://www.bde.es/webbe/es/estadisticas/compartido/datos/zip/{zid}.zip", timeout=(10,180))
    resp.raise_for_status()
    zf = zipfile.ZipFile(io.BytesIO(resp.content))
    names = [n for n in zf.namelist() if n.endswith(".csv") and not n.startswith("catalogo")]
    sample = names[:2] if zid == "ti" else ["be0101.csv", "be0115.csv"]
    for name in sample:
        text = zf.read(name).decode("latin-1")
        rows, skipped = parse_csv(text)
        print(f"\n{zid}/{name}: {len(rows)} long rows; skipped labels sample: {sorted(skipped)[:6]}")
        for row in rows[:3]:
            print("   ", row)
        # last rows to confirm footer not parsed
        for row in rows[-2:]:
            print("   ...", row)
