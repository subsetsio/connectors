import io, zipfile, tempfile, csv, collections
from subsets_utils import get, get_client

def dl(url):
    tmp=tempfile.NamedTemporaryFile(suffix=".zip", delete=False)
    with get_client().stream("GET", url, timeout=(10,300)) as r:
        r.raise_for_status()
        for c in r.iter_bytes(1<<20): tmp.write(c)
    tmp.close(); return zipfile.ZipFile(tmp.name)

# co2e_100yr country package for ABW: which sectors/subsectors present in country_emissions?
for gas in ["co2e_100yr","co2"]:
    url=f"https://downloads.climatetrace.org/latest/country_packages/{gas}/ABW.zip"
    try:
        zf=dl(url)
    except Exception as e:
        print(gas,"ERR",e); continue
    ce=[n for n in zf.namelist() if "_country_emissions_" in n and n.endswith(".csv")]
    sectors=set(); subs=set(); gases=collections.Counter()
    for n in ce:
        with zf.open(n) as f:
            rdr=csv.DictReader(io.TextIOWrapper(f,encoding="utf-8"))
            for row in rdr:
                sectors.add(row["sector"]); subs.add(row["subsector"]); gases[row["gas"]]+=1
    print(f"\n=== {gas} ABW country pkg: {len(ce)} CE files ===")
    print("sectors:", sorted(sectors))
    print("n subsectors:", len(subs))
    print("gases:", dict(gases))
