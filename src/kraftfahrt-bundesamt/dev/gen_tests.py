import json, os
COLLECT="/Users/nathansnellaert/Documents/hardened/data/sources/kraftfahrt-bundesamt/assets/collect/entities/current.json"
UNION="/Users/nathansnellaert/Documents/hardened/data/sources/kraftfahrt-bundesamt/work/entity_union.json"
d=json.load(open(COLLECT))
# unwrap to entity dict
def entries(d):
    if isinstance(d,dict) and all(isinstance(v,dict) and 'name' in v for v in d.values()): return d
    for k in ('entries','catalog','entities','data'):
        if isinstance(d,dict) and isinstance(d.get(k),dict): return d[k]
    return d
ents=entries(d)
union=json.load(open(UNION))

PREFIX="kraftfahrt-bundesamt-"
# ordered period/time-dimension candidates (exact source field names incl. typo)
PERIOD=["Berichtszeitpunkt","Berichstzeitpunkt","Berichtszeitraum","Berichtsjahr","berichtsj","Jahr"]
INT_TYPES={"esriFieldTypeInteger","esriFieldTypeSmallInteger","esriFieldTypeOID"}
COUNT=["Anzahl","Fahrten"]

os.makedirs("tests",exist_ok=True)
def y(v):
    return v
for slug in union:
    e=ents[slug]
    fields=e["source_metadata"].get("fields",[])
    fnames=[f["name"] for f in fields]
    ftype={f["name"]:f.get("type") for f in fields}
    spec_id=f"{PREFIX}{slug}"
    lines=[f"spec_id: {spec_id}","status: active","tests:"]
    lines.append("  - row_count: {min: 1}")
    lines.append("    reason: every KBA Statistikportal layer is a populated official table")
    lines.append("    certainty: 90")
    # period not_null
    per=next((c for c in PERIOD if c in fnames),None)
    if per:
        lines.append(f"  - not_null: {per}")
        lines.append(f"    reason: {per} is the primary reporting-period dimension; never suppressed")
        lines.append("    certainty: 85")
    # count column_type integer (warn — NDJSON inference)
    cnt=next((c for c in COUNT if c in fnames and ftype.get(c) in INT_TYPES),None)
    if cnt:
        lines.append(f"  - column_type: {{col: {cnt}, type: integer}}")
        lines.append(f"    reason: {cnt} is an esriFieldTypeInteger count")
        lines.append("    certainty: 75")
        lines.append("    severity: warn")
    open(f"tests/{spec_id}.yaml","w").write("\n".join(lines)+"\n")
    print(f"{spec_id}: period={per} count={cnt} fields={len(fnames)}")
print("wrote",len(union),"yaml files")
