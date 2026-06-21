import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import io, zipfile, csv
from collections import Counter
from subsets_utils import get

def probe(url):
    print("="*70)
    print("URL:", url)
    r = get(url, timeout=(10,120))
    print("status", r.status_code, "bytes", len(r.content))
    zf = zipfile.ZipFile(io.BytesIO(r.content))
    names = zf.namelist()
    print("zip members:", names)
    with zf.open(names[0]) as f:
        text = io.TextIOWrapper(f, encoding="utf-8")
        rdr = csv.reader(text)
        header = next(rdr)
        print("header:", header)
        rows = []
        sats = Counter(); biomas = Counter(); paises = Counter()
        n = 0
        for row in rdr:
            n += 1
            d = dict(zip(header, row))
            if n <= 3: rows.append(d)
            sats[d.get("satelite","")] += 1
            biomas[d.get("bioma","")] += 1
            paises[d.get("pais","")] += 1
            if n >= 200000: break
        print("sample rows:")
        for d in rows: print("  ", d)
        print("rows scanned:", n)
        print("satelites:", sats.most_common(8))
        print("biomas:", biomas.most_common(8))
        print("paises:", paises.most_common(8))

probe("https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/Brasil_sat_ref/focos_br_ref_2023.zip")
probe("https://dataserver-coids.inpe.br/queimadas/queimadas/focos/csv/anual/AMS_sat_ref/focos_ams_ref_2023.zip")
