"""Dry-run the YAML assertions against the dev/tmp ndjson dumps, replicating the
harness test_engine's SQL so I can catch authoring mistakes before evaluate."""
import glob, os, re, datetime
import duckdb, yaml

HERE = os.path.dirname(__file__)
TESTS = os.path.join(HERE, "..", "tests")
TMP = os.path.join(HERE, "tmp")
SLUG = "central-bank-of-nigeria"
con = duckdb.connect()
THIS_YEAR = datetime.date.today().year
TODAY = datetime.date.today()


def entity_of(sid):
    # reverse map via the tmp files
    for p in glob.glob(os.path.join(TMP, "*.ndjson")):
        e = os.path.basename(p)[:-7]
        if f"{SLUG}-{e.lower()}" == sid:
            return p
    return None


def resolve(expr):
    if isinstance(expr, str):
        if expr == "current_year()":
            return THIS_YEAR
        m = re.match(r"today\s*-\s*(\d+)d", expr)
        if m:
            return (TODAY - datetime.timedelta(days=int(m.group(1)))).isoformat()
        if expr == "today":
            return TODAY.isoformat()
    return expr


def col(c):
    return '"' + c.replace('"', '""') + '"'


fails = []
for path in sorted(glob.glob(os.path.join(TESTS, "*.yaml"))):
    doc = yaml.safe_load(open(path))
    sid = doc["spec_id"]
    src = entity_of(sid)
    if not src:
        print("NO DATA for", sid); continue
    rel = f"read_json_auto('{src}')"
    n = con.execute(f"SELECT count(*) FROM {rel}").fetchone()[0]
    for t in doc.get("tests", []):
        keys = [k for k in t if k not in ("reason", "certainty", "points_outward", "severity")]
        kind = keys[0]; p = t[kind]
        try:
            if kind == "not_null":
                bad = con.execute(f"SELECT count(*) FROM {rel} WHERE {col(p)} IS NULL").fetchone()[0]
                ok = bad == 0; obs = f"{bad} nulls"
            elif kind == "unique":
                cols = p if isinstance(p, list) else [p]
                tup = ",".join(col(c) for c in cols)
                bad = con.execute(f"SELECT count(*)-count(DISTINCT ({tup})) FROM {rel}").fetchone()[0]
                ok = bad == 0; obs = f"{bad} dups"
            elif kind == "column_type":
                typ = con.execute(f"SELECT any_value(typeof({col(p['col'])})) FROM {rel}").fetchone()[0]
                fam = {"integer": ("BIGINT", "INTEGER", "HUGEINT"), "float": ("DOUBLE", "DECIMAL", "FLOAT"),
                       "string": ("VARCHAR",), "date": ("DATE",), "timestamp": ("TIMESTAMP",), "boolean": ("BOOLEAN",)}[p["type"]]
                ok = any(typ.upper().startswith(f) for f in fam); obs = typ
            elif kind == "matches":
                bad = con.execute(f"SELECT count(*) FROM {rel} WHERE {col(p['col'])} IS NOT NULL AND NOT regexp_full_match(CAST({col(p['col'])} AS VARCHAR), ?)", [p["pattern"]]).fetchone()[0]
                ok = bad == 0; obs = f"{bad} unmatched"
            elif kind == "row_count":
                lo, hi = p.get("min"), p.get("max")
                ok = (lo is None or n >= lo) and (hi is None or n <= hi); obs = n
            elif kind == "enum":
                vals = ",".join("'" + str(v).replace("'", "''") + "'" for v in p["values"])
                bad = con.execute(f"SELECT count(*) FROM {rel} WHERE {col(p['col'])} IS NOT NULL AND {col(p['col'])} NOT IN ({vals})").fetchone()[0]
                ok = bad == 0; obs = f"{bad} outside"
            elif kind == "distinct_count":
                d = con.execute(f"SELECT approx_count_distinct({col(p['col'])}) FROM {rel}").fetchone()[0]
                lo, hi = p.get("min"), p.get("max")
                ok = (lo is None or d >= lo) and (hi is None or d <= hi); obs = d
            elif kind in ("between", "at_most", "at_least", "freshness"):
                mn, mx = con.execute(f"SELECT min({col(p['col'])}), max({col(p['col'])}) FROM {rel}").fetchone()
                def num(x):
                    try: return float(x)
                    except: return x
                if kind == "between":
                    lo, hi = resolve(p["lo"]), resolve(p["hi"])
                    ok = num(mn) >= num(lo) and num(mx) <= num(hi); obs = f"[{mn},{mx}]"
                elif kind == "at_most":
                    v = resolve(p["expr"]); ok = num(mx) <= num(v); obs = mx
                elif kind == "at_least":
                    v = resolve(p["expr"]); ok = num(mn) >= num(v); obs = mn
                else:  # freshness
                    v = resolve(p["reaches"]); ok = str(mx) >= str(v); obs = f"max={mx} reaches={v}"
            elif kind in ("mean_between", "median_between"):
                fn = "avg" if kind == "mean_between" else "median"
                v = con.execute(f"SELECT {fn}(TRY_CAST({col(p['col'])} AS DOUBLE)) FROM {rel}").fetchone()[0]
                ok = v is not None and p["lo"] <= v <= p["hi"]; obs = round(v, 4) if v is not None else None
            else:
                ok = None; obs = "UNCHECKED"
        except Exception as e:
            ok = None; obs = f"ERR {type(e).__name__}: {e}"
        sev = t.get("severity", "block")
        if ok is not True:
            fails.append((sid, kind, p, obs, ok, sev, t.get("certainty")))

print(f"\n=== {len(fails)} non-passing assertions ===")
for sid, kind, p, obs, ok, sev, cert in fails:
    flag = "ERROR" if ok is None else "FAIL"
    print(f"[{flag}/{sev}/c{cert}] {sid.replace(SLUG+'-','')} {kind}={p} -> {obs}")
