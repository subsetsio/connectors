import gzip, json
from subsets_utils import get

M = {"mailto": "nathansnellaert@gmail.com"}
S3 = "https://openalex.s3.amazonaws.com"

# --- 1. S3 manifest + one record per reference entity ---
for ent in ["fields", "sdgs", "topics", "funders"]:
    man = get(f"{S3}/data/{ent}/manifest", timeout=60).json()
    entries = man["entries"]
    total = sum(e["meta"]["record_count"] for e in entries)
    print(f"\n=== {ent}: {len(entries)} partitions, {total} records ===")
    # fetch first non-empty partition, first record
    for e in entries:
        url = e["url"].replace("s3://openalex/", f"{S3}/")
        raw = gzip.decompress(get(url, timeout=120).content)
        line = raw.split(b"\n", 1)[0]
        if line.strip():
            rec = json.loads(line)
            print("KEYS:", sorted(rec.keys()))
            if ent == "fields":
                print("  domain:", rec.get("domain"))
                print("  ids:", rec.get("ids"))
            if ent == "topics":
                print("  domain:", rec.get("domain"), "| field:", rec.get("field"), "| subfield:", rec.get("subfield"))
            if ent == "funders":
                print("  summary_stats:", rec.get("summary_stats"), "| ids:", rec.get("ids"))
            break

# --- 2. group_by enumerate + filter syntax for each dimension ---
print("\n\n===== group_by dimensions =====")
DIMS = {
    "type": ("type", "type"),
    "oa_status": ("open_access.oa_status", "open_access.oa_status"),
    "domain": ("primary_topic.domain.id", "primary_topic.domain.id"),
    "field": ("primary_topic.field.id", "primary_topic.field.id"),
    "sdg": ("sustainable_development_goals.id", "sustainable_development_goals.id"),
}
for name, (gb, filt) in DIMS.items():
    d = get("https://api.openalex.org/works", params={**M, "group_by": gb}, timeout=60).json()
    groups = d["group_by"]
    print(f"\n{name}: groups_count={d['meta']['groups_count']} sample={[(g['key'], g['key_display_name'], g['count']) for g in groups[:2]]}")
    # try filtering by the first key, group by year
    k = groups[0]["key"]
    d2 = get("https://api.openalex.org/works", params={**M, "filter": f"{filt}:{k}", "group_by": "publication_year"}, timeout=60).json()
    yr = d2["group_by"]
    print(f"  filter {filt}:{k} -> meta.count={d2['meta']['count']} year_groups={len(yr)} top={[(g['key'], g['count']) for g in yr[:3]]}")
