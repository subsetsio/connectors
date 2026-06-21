import csv, io
from subsets_utils import get

ids = ["DF_DES_SEXO","DF_ICL2023","DF_BGREIMPROMSP","DF_NMIC_SEXO",
       "DF_IR2023_RAMA","DF_HRS_TNR_SEXO","DF_OCUCIUO_CIUO88_SEXO","DF_NPGU_SEXO"]
for did in ids:
    url = f"https://sdmx.ine.gob.cl/rest/data/CL01,{did},1.0?format=csv"
    r = get(url, headers={"Accept":"application/vnd.sdmx.data+csv"}, timeout=(10,120))
    txt = r.text
    rows = list(csv.reader(io.StringIO(txt)))
    hdr = rows[0] if rows else []
    data = rows[1:]
    vi = hdr.index("OBS_VALUE") if "OBS_VALUE" in hdr else -1
    ti = hdr.index("TIME_PERIOD") if "TIME_PERIOD" in hdr else -1
    nonnull = sum(1 for d in data if vi>=0 and len(d)>vi and d[vi].strip()!="")
    times = sorted({d[ti] for d in data if ti>=0 and len(d)>ti}) if ti>=0 else []
    print(f"{did}: status={r.status_code} ncols={len(hdr)} nrows={len(data)} obs_nonnull={nonnull} time[{times[0] if times else '?'}..{times[-1] if times else '?'}]")
    print("   cols:", hdr)
