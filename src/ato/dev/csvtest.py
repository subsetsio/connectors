import csv, io, collections
from subsets_utils import get
from utils import build_groups
groups = build_groups()

# pick a few CSV taxation-statistics entities
import json
coll=json.load(open('/Users/nathansnellaert/Documents/hardened/data/sources/ato/assets/collect/entities/current.json'))
csv_ents=[k for k,e in coll.items() if any('CSV' in f.upper() for f in e['source_metadata'].get('formats',[]))]
print("csv entities:", len(csv_ents))
yrcov=collections.Counter()
for k in csv_ents:
    yrs=tuple(sorted(set(r['income_year'] for r in groups[k] if (r['format'] or '').upper()=='CSV' and r['income_year'])))
    yrcov[yrs]+=1
print("year-coverage distribution (CSV resources):")
for y,c in yrcov.most_common(8): print("  ",c,"entities ->",y)

# direct download test on one
ent="taxation-statistics--financialratios4trusts1c-csv"
for r in groups[ent]:
    if (r['format'] or '').upper()!='CSV': continue
    # need the resource url; build_groups didn't keep it -> fetch package? use ckan resource_show
    rs=get("https://data.gov.au/data/api/3/action/resource_show",params={"id":r['resource_id']},timeout=(10,120))
    rs.raise_for_status(); url=rs.json()["result"]["url"]
    print("\nyear",r['income_year'],"url",url)
    resp=get(url,timeout=(10,120)); resp.raise_for_status()
    text=resp.content.decode('utf-8-sig',errors='replace')
    rdr=csv.DictReader(io.StringIO(text))
    rows=list(rdr)
    print("  ncols",len(rdr.fieldnames or []),"cols",rdr.fieldnames[:8])
    print("  nrows",len(rows),"row0",dict(list(rows[0].items())[:5]) if rows else None)
    break
