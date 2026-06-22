import sys, io, traceback
sys.path.insert(0, "src")
import subsets_utils
from subsets_utils import get
import openpyxl

BASE = "https://live.laborstats.alaska.gov"

def fetch(url):
    try:
        r = get(url, timeout=(10, 120))
        return r
    except Exception as e:
        print(f"  ERROR fetching: {e}")
        return None

def probe_csv(url, nlines=6):
    print(f"\n=== CSV: {url}")
    r = fetch(url)
    if r is None: return
    print(f"  status={r.status_code} ctype={r.headers.get('content-type')} len={len(r.content)}")
    if r.status_code != 200:
        return
    text = r.content.decode("utf-8", errors="replace")
    for i, line in enumerate(text.splitlines()[:nlines]):
        print(f"  L{i+1}: {line[:300]}")

def probe_xlsx(url, sheet_rows=10):
    print(f"\n=== XLSX: {url}")
    r = fetch(url)
    if r is None: return
    print(f"  status={r.status_code} ctype={r.headers.get('content-type')} len={len(r.content)}")
    if r.status_code != 200:
        return
    ro = False
    try:
        wb = openpyxl.load_workbook(io.BytesIO(r.content), data_only=True)
    except Exception as e:
        try:
            wb = openpyxl.load_workbook(io.BytesIO(r.content), data_only=True, read_only=True)
            ro = True
        except Exception as e2:
            print(f"  NOT a valid xlsx: {e} / {e2}")
            print("  first bytes:", r.content[:120])
            return
    print(f"  sheets: {wb.sheetnames}  (read_only={ro})")
    ws = wb[wb.sheetnames[0]]
    if not ro:
        print(f"  primary sheet '{ws.title}' max_row={ws.max_row} max_col={ws.max_column}")
    else:
        print(f"  primary sheet '{ws.title}'")
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        if i >= sheet_rows: break
        cells = [("" if c is None else str(c))[:22] for c in row]
        print(f"  R{i+1}: {cells}")

def head(url):
    r = fetch(url)
    if r is None:
        print(f"  {url} -> ERR")
        return None
    print(f"  {url} -> {r.status_code} {r.headers.get('content-type')} {len(r.content)}b")
    return r

if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else ""
    args = sys.argv[2:]
    if cmd == "csv":
        for u in args: probe_csv(u)
    elif cmd == "xlsx":
        for u in args: probe_xlsx(u)
    elif cmd == "head":
        for u in args: head(u)
    else:
        print("usage: probe.py [csv|xlsx|head] URL...")
