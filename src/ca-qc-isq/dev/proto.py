import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, re, io, urllib.parse
from subsets_utils import get
import lxml.html

NBSP = "\xa0"
MISSING = {"", "..", "...", "....", "n.d.", "nd", "x", "F", "..F", "s.o.", "so", "n/a", "na", "-", "–", "—", "*", "r", "p", "e"}
_TAG = re.compile(r"<[^>]+>")
_SUP = re.compile(r"[¹²³⁰-₟]+")  # superscript footnote marks

def clean_text(s):
    if s is None: return ""
    s = _TAG.sub(" ", str(s))
    s = s.replace(NBSP, " ").replace(" ", " ")
    s = _SUP.sub("", s)
    return re.sub(r"\s+", " ", s).strip()

def to_num(s):
    t = s.replace(" ", "").replace(NBSP, "")
    if t in MISSING or t == "": return None
    # strip footnote letters/symbols around number
    t = re.sub(r"[^\d,.\-]", "", t)
    if t in ("", "-", ".", ","): return None
    if "," in t and "." in t:
        t = t.replace(",", "")          # comma thousands, dot decimal
    elif "," in t:
        t = t.replace(",", ".")         # comma decimal
    try: return float(t)
    except: return None

def melt(headers, data):
    width = max([len(r) for r in headers+data] or [0])
    H = [r+[""]*(width-len(r)) for r in headers]
    D = [r+[""]*(width-len(r)) for r in data]
    keep = [j for j in range(width) if any((H[r][j] or "").strip() for r in range(len(H))) or any((D[i][j] or "").strip() for i in range(len(D)))]
    valcols = [j for j in keep if any(to_num(D[i][j]) is not None for i in range(len(D)))]
    labcols = [j for j in keep if j not in valcols]
    def col_label(j):
        parts = [clean_text(H[r][j]) for r in range(len(H)) if clean_text(H[r][j])]
        return " | ".join(dict.fromkeys(parts)) or f"col{j}"
    out=[]
    if not valcols or not D:
        for i,row in enumerate(D):
            for j in keep:
                v = clean_text(row[j])
                if v: out.append((i, f"row{i}", col_label(j), v, to_num(row[j])))
        return out
    for i,row in enumerate(D):
        rl = " | ".join([clean_text(row[j]) for j in labcols if clean_text(row[j])]) or f"row{i}"
        for j in valcols:
            raw = clean_text(row[j])
            if raw == "": continue
            out.append((i, rl, col_label(j), raw, to_num(row[j])))
    return out

def page_data(slug):
    for lang in ("en","fr"):
        r = get(f"https://statistique.quebec.ca/{lang}/produit/tableau/{slug}", timeout=(10,40))
        if r.status_code==200:
            m = re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>', r.text, re.S)
            if m: return json.loads(m.group(1))["props"]["pageProps"]["data"]
    return None

def flatten_cols(nodes, anc=()):
    leaves=[]
    for nd in nodes:
        if not isinstance(nd, dict): continue
        title = nd.get("title","")
        sub = nd.get("columns")
        if sub:
            leaves += flatten_cols(sub, anc+((title,) if title else ()))
        elif nd.get("field"):
            label = " | ".join([t for t in anc+((title,) if title else anc) if t]) or nd["field"]
            # build label from ancestors + own title
            full = [t for t in anc if t] + ([title] if title else [])
            leaves.append((nd["field"], " | ".join(full) or nd["field"]))
    return leaves

def dynamic_grid(no):
    h = get(f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_header?p_id_tabl={no}", timeout=(10,60))
    cfg = json.loads(h.text)["tableConfig"]
    cols = flatten_cols(cfg.get("columns",[]))
    fields = [f for f,_ in cols]
    labels = [lab for _,lab in cols]
    champs = urllib.parse.quote(",".join(fields))
    d = get(f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_data?p_id_tabl={no}&p_champs={champs}", timeout=(10,90))
    import csv as csvmod
    rows = list(csvmod.reader(io.StringIO(d.text), delimiter=";"))
    # first row is the field codes; replace with labels
    body = rows[1:] if rows else []
    return [labels], body

def static_grid(html):
    doc = lxml.html.fromstring(html)
    tbl = doc.find(".//table")
    grid_rows=[]; rowspans={}
    head_count=0
    for tr in tbl.iterfind(".//tr"):
        cells = tr.xpath("./th|./td")
        row=[]; j=0
        # apply pending rowspans
        is_header = all(c.tag=="th" for c in cells) and len(cells)>0
        out=[]
        col=0
        pend = rowspans
        # simpler: build with colspan only, ignore rowspan complexity for proto
        for c in cells:
            cs = int(c.get("colspan",1) or 1)
            txt = c.text_content()
            for _ in range(cs): out.append(txt)
        grid_rows.append((is_header, out))
    headers=[r for h,r in grid_rows if h]
    data=[r for h,r in grid_rows if not h]
    return headers, data

for tag,slug in [("DYN-4625-pop","population-composantes-accroissement-demographique-trimestre-quebec"),
                 ("DYN-4744-gdp","gross-domestic-product-expenditure-quebec")]:
    d=page_data(slug)
    H,D = dynamic_grid(d["no"])
    rows = melt(H,D)
    print(f"\n### {tag}  header_cols={len(H[0])} data_rows={len(D)} -> melted={len(rows)}")
    for r in rows[:6]: print("   ", tuple(str(x)[:30] for x in r))

# static
sd = page_data("person-years-wage-bill-and-paid-hours-for-core-drilling-quebec")
H,D = static_grid(sd["html"])
rows = melt(H,D)
print(f"\n### STAT-forage header_rows={len(H)} data_rows={len(D)} -> melted={len(rows)}")
for r in rows[:8]: print("   ", tuple(str(x)[:30] for x in r))
