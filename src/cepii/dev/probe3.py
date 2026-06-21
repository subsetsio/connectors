import io, re, zipfile
from subsets_utils import get

def magic(url, n=16):
    r = get(url, headers={"Range": f"bytes=0-{n-1}"}, timeout=(10, 60))
    return r.content[:n]

def head(url):
    r = get(url, headers={"Range": "bytes=0-0"}, timeout=(10, 60))
    return r.status_code, r.headers.get("content-type"), r.headers.get("content-range")

def members_small(url):
    r = get(url, timeout=(10, 120)); r.raise_for_status()
    z = zipfile.ZipFile(io.BytesIO(r.content))
    return [(i.filename, i.file_size) for i in z.infolist()]

def members_tail(url, tail=300_000):
    s, ct, cr = head(url)
    total = int(cr.split("/")[-1]) if cr else None
    start = max(0, (total or tail) - tail)
    r = get(url, headers={"Range": f"bytes={start}-"}, timeout=(10, 120))
    data = r.content
    names = []
    for m in re.finditer(b"PK\x01\x02", data):
        off = m.start()
        try:
            nlen = int.from_bytes(data[off+28:off+30], "little")
            fsize = int.from_bytes(data[off+24:off+28], "little")
            name = data[off+46:off+46+nlen].decode("utf-8", "replace")
            names.append((name, fsize))
        except Exception:
            pass
    return total, names

CHECK_MAGIC = {
 "geodist_zip": "https://www.cepii.fr/distance/dist_cepii.zip",
 "geodep_csv": "https://www.cepii.fr/DATA_DOWNLOAD/geodep/geodep_data.csv",
 "protee_csv": "https://www.cepii.fr/DATA_DOWNLOAD/ProTEE/ProTEE_0_1.csv",
 "eqchange_reer_xls": "https://www.cepii.fr/DATA_DOWNLOAD/EQCHANGE/186_TP/Weights_TV/EER/Indices/Annual/CPI_based/REER_Weights_TV.xls",
 "rprod_xls": "https://www.cepii.fr/DATA_DOWNLOAD/EQCHANGE/RPROD.xls",
 "language_dta": "https://www.cepii.fr/DATA_DOWNLOAD/language/ling_web.dta",
 "trade_volume_zip": "https://www.cepii.fr/DATA_DOWNLOAD/trade_volume/data/trade_volume_v202507.zip",
}
print("== MAGIC / HEAD ==")
for k, u in CHECK_MAGIC.items():
    try:
        print(f"{k:20} {head(u)} magic={magic(u)!r}")
    except Exception as e:
        print(f"{k:20} ERR {e}")

SMALL_ZIPS = {
 "econmap": "https://www.cepii.fr/DATA_DOWNLOAD/baseline/v3.1/EconMap_3_1.zip",
 "macmap": "https://www.cepii.fr/DATA_DOWNLOAD/macmap/download/mmhs2_2007.zip",
 "intense": "https://www.cepii.fr/DATA_DOWNLOAD/IntenSE/IntenSE_2025_v1.zip",
}
print("\n== SMALL ZIP MEMBERS ==")
for k, u in SMALL_ZIPS.items():
    try:
        print(f"-- {k}")
        for n, s in members_small(u):
            print(f"     {s:>12}  {n}")
    except Exception as e:
        print(f"   {k} ERR {e}")

BIG_ZIPS = {
 "baci_hs92": "https://www.cepii.fr/DATA_DOWNLOAD/baci/data/BACI_HS92_V202601.zip",
 "gravity": "https://www.cepii.fr/DATA_DOWNLOAD/gravity/data/Gravity_csv_V202211.zip",
 "chelem_trade": "https://www.cepii.fr/DATA_DOWNLOAD/chelem/data/202502/chelem_trade_v202502.zip",
 "tradeprod": "https://www.cepii.fr/DATA_DOWNLOAD/tradeprod/V202401/TPc_V202401_csv.zip",
 "tuv_hs12_x": "https://www.cepii.fr/DATA_DOWNLOAD/TUV/data/TUV_HS12_x_V202104.zip",
 "wtfc": "https://www.cepii.fr/DATA_DOWNLOAD/WTFC/data/WTFC_HS96_V202104.zip",
}
print("\n== BIG ZIP MEMBERS (tail parse) ==")
for k, u in BIG_ZIPS.items():
    try:
        total, names = members_tail(u)
        print(f"-- {k} total={total}")
        for n, s in names:
            print(f"     {s:>14}  {n}")
    except Exception as e:
        print(f"   {k} ERR {e}")
