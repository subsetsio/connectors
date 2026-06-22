import json, os

COLLECT = "/Users/nathansnellaert/Documents/hardened/data/sources/dares/assets/collect/entities/current.json"
OUT = "/Users/nathansnellaert/Documents/hardened/connectors/src/dares/tests"
os.makedirs(OUT, exist_ok=True)

d = json.load(open(COLLECT))
ents = d['entities'] if 'entities' in d and isinstance(d['entities'], dict) else d

TYPEMAP = {"text":"string","double":"float","int":"integer","integer":"integer",
           "date":"date","datetime":"timestamp","boolean":"boolean","geo_point_2d":"string"}

def spec_id(eid): return "dares-" + eid.lower().replace("_","-")

def y(s): return s  # plain strings, no special chars expected

for eid, ent in ents.items():
    sm = ent["source_metadata"]
    ftypes = sm.get("field_types") or {}
    fnames = sm.get("field_names") or list(ftypes.keys())
    rec = sm.get("records_count") or 0
    sid = spec_id(eid)
    # key column: prefer 'date', else first field
    keycol = "date" if "date" in fnames else (fnames[0] if fnames else None)
    # numeric value column
    numcol = next((f for f in fnames if ftypes.get(f) in ("double","int","integer")), None)
    floor = max(1, int(rec * 0.4))

    lines = []
    lines.append(f"spec_id: {sid}")
    lines.append("status: active")
    lines.append("tests:")
    lines.append(f"  - row_count: {{min: {floor}}}")
    lines.append(f"    reason: full one-shot ODS parquet export; source reports ~{rec} records, a large shortfall means a truncated download")
    lines.append("    certainty: 80")
    if keycol:
        lines.append(f"  - not_null: {keycol}")
        lines.append(f"    reason: '{keycol}' is a dimension key present on every row of this table")
        lines.append("    certainty: 90")
        ktype = TYPEMAP.get(ftypes.get(keycol), "string")
        lines.append(f"  - column_type: {{col: {keycol}, type: {ktype}}}")
        lines.append("    certainty: 85")
    if numcol and numcol != keycol:
        ntype = TYPEMAP.get(ftypes.get(numcol), "float")
        lines.append(f"  - column_type: {{col: {numcol}, type: {ntype}}}")
        lines.append(f"    reason: '{numcol}' carries the numeric measure for this statistical table")
        lines.append("    certainty: 80")
    with open(os.path.join(OUT, sid + ".yaml"), "w") as f:
        f.write("\n".join(lines) + "\n")

print("wrote", len(ents), "yaml files to", OUT)
