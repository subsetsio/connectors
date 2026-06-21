import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import json, re, io, urllib.parse, csv as csvmod
from subsets_utils import get
import lxml.html

NBSP="\xa0"; NNBSP=" "
MISSING={"","..","...","....","n.d.","nd","x","f","..f","s.o.","so","n/a","na","-","–","—","*"}
_TAG=re.compile(r"<[^>]+>"); _SUP=re.compile(r"[¹²³⁰-₟]+")

def clean_text(s):
    if s is None: return ""
    s=_TAG.sub(" ",str(s)).replace(NBSP," ").replace(NNBSP," ")
    s=_SUP.sub("",s)
    return re.sub(r"\s+"," ",s).strip()

def to_num(s):
    t=str(s).replace(" ","").replace(NBSP,"").replace(NNBSP,"")
    if t.lower() in MISSING or t=="": return None
    t=re.sub(r"[^\d,.\-]","",t)
    if not re.search(r"\d",t): return None
    if "," in t and "." in t:
        if t.rfind(".")>t.rfind(","): t=t.replace(",","")      # dot decimal, comma thousands
        else: t=t.replace(".","").replace(",",".")              # comma decimal, dot thousands
    elif "," in t:
        if re.fullmatch(r"-?\d{1,3}(,\d{3})+",t): t=t.replace(",","")   # comma thousands
        else: t=t.replace(",",".")                                       # comma decimal
    elif "." in t:
        if re.fullmatch(r"-?\d{1,3}(\.\d{3})+",t): t=t.replace(".","")   # dot thousands
    try: return float(t)
    except: return None

def melt(headers,data):
    width=max([len(r) for r in headers+data] or [0])
    H=[r+[""]*(width-len(r)) for r in headers]; D=[r+[""]*(width-len(r)) for r in data]
    keep=[j for j in range(width) if any(clean_text(H[r][j]) for r in range(len(H))) or any(clean_text(D[i][j]) for i in range(len(D)))]
    def numeric_col(j):
        vals=[D[i][j] for i in range(len(D)) if clean_text(D[i][j])]
        if not vals: return False
        nums=sum(1 for v in vals if to_num(v) is not None)
        return nums>=max(1,0.5*len(vals))
    # col0 always label; labels = leading prefix until first numeric column
    first_val=None
    for idx,j in enumerate(keep):
        if idx==0: continue
        if numeric_col(j): first_val=idx; break
    if first_val is None: first_val=min(1,len(keep))
    labcols=keep[:first_val]; valcols=[j for j in keep[first_val:] if numeric_col(j)]
    def col_label(j):
        parts=[clean_text(H[r][j]) for r in range(len(H)) if clean_text(H[r][j])]
        return " | ".join(dict.fromkeys(parts)) or f"col{j}"
    out=[]
    if not valcols:
        for i,row in enumerate(D):
            rl=" | ".join(clean_text(row[j]) for j in labcols if clean_text(row[j])) or f"row{i}"
            for j in keep:
                v=clean_text(row[j])
                if v: out.append((i,rl,col_label(j),v,to_num(row[j])))
        return out
    for i,row in enumerate(D):
        rl=" | ".join(clean_text(row[j]) for j in labcols if clean_text(row[j])) or f"row{i}"
        for j in valcols:
            raw=clean_text(row[j])
            if raw=="": continue
            out.append((i,rl,col_label(j),raw,to_num(row[j])))
    return out

def page_data(slug):
    for lang in ("en","fr"):
        r=get(f"https://statistique.quebec.ca/{lang}/produit/tableau/{slug}",timeout=(10,40))
        if r.status_code==200:
            m=re.search(r'<script id="__NEXT_DATA__"[^>]*>(.*?)</script>',r.text,re.S)
            if m: return json.loads(m.group(1))["props"]["pageProps"]["data"]
    return None

def flatten_cols(nodes,anc=()):
    leaves=[]
    for nd in nodes:
        if not isinstance(nd,dict): continue
        title=nd.get("title","") or ""
        sub=nd.get("columns")
        if sub: leaves+=flatten_cols(sub,anc+((title,) if title else ()))
        elif nd.get("field"):
            full=[t for t in anc if t]+([title] if title else [])
            leaves.append((nd["field"]," | ".join(full) or nd["field"]))
    return leaves

def dynamic_grid(no):
    h=get(f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_header?p_id_tabl={no}",timeout=(10,60))
    cfg=json.loads(h.text)["tableConfig"]; cols=flatten_cols(cfg.get("columns",[]))
    fields=[f for f,_ in cols]; labels=[lab for _,lab in cols]
    champs=urllib.parse.quote(",".join(fields))
    d=get(f"https://statistique.quebec.ca/pls/ken/ken411_data_explt_v2.p_retrn_data?p_id_tabl={no}&p_champs={champs}",timeout=(10,90))
    rows=list(csvmod.reader(io.StringIO(d.text),delimiter=";"))
    return [labels], rows[1:]

def static_grid(html):
    tbl=lxml.html.fromstring(html).find(".//table")
    grid=[]
    for tr in tbl.iterfind(".//tr"):
        cells=tr.xpath("./th|./td")
        if not cells: continue
        is_h=all(c.tag=="th" for c in cells)
        out=[]
        for c in cells:
            cs=int(c.get("colspan",1) or 1)
            for _ in range(cs): out.append(c.text_content())
        grid.append((is_h,out))
    return [r for h,r in grid if h],[r for h,r in grid if not h]

tests=[("DYN-4625-pop","population-composantes-accroissement-demographique-trimestre-quebec","dyn"),
       ("DYN-4744-gdp","gross-domestic-product-expenditure-quebec","dyn"),
       ("STAT-forage","person-years-wage-bill-and-paid-hours-for-core-drilling-quebec","stat"),
       ("life-exp","life-expectancy-at-birth-and-at-65-years-by-sex","auto"),
       ("first-marriage","first-marriage-rates-by-age-group-and-sex-quebec","auto")]
for tag,slug,kind in tests:
    d=page_data(slug)
    if d is None: print(tag,"PAGEFAIL"); continue
    if d.get("type")=="dynamique": H,D=dynamic_grid(d["no"])
    elif d.get("type")=="statique": H,D=static_grid(d.get("html") or "")
    else: print(tag,"type",d.get("type")); continue
    rows=melt(H,D)
    nnum=sum(1 for r in rows if r[4] is not None)
    print(f"\n### {tag} [{d.get('type')}] rows={len(rows)} num={nnum}")
    for r in rows[:5]: print("   ",tuple(str(x)[:34] for x in r))
