import sys, os; sys.path.insert(0, os.path.join(os.path.dirname(__file__),"..","src"))
import io, pandas as pd
from subsets_utils import get

BASE = "https://cdn.bancentral.gov.do/"
samples = {
  "ipc_base": "documents/estadisticas/precios/documents/ipc_base_2019-2020.xls",
  "tasas_diariasBAC": "documents/estadisticas/sector-monetario-y-financiero/documents/tasas_diariasBAC-2024.xls",
  "pib": "documents/estadisticas/sector-real/documents/pib.xls",
  "tasa_desocupacion_fa": "documents/estadisticas/mercado-de-trabajo/documents/tasa_desocupacion_fa.xls",
  "lleg_total": "documents/estadisticas/sector-turismo/documents/lleg_total.xls",
}
for name, path in samples.items():
    print("="*70)
    print(name, path)
    try:
        r = get(BASE+path, timeout=(10,120))
        print("status", r.status_code, "bytes", len(r.content), "ctype", r.headers.get("content-type"))
        if r.status_code != 200: continue
        bio = io.BytesIO(r.content)
        try:
            xls = pd.ExcelFile(bio)
        except Exception as e:
            print("  ExcelFile err:", type(e).__name__, e); continue
        print("  sheets:", xls.sheet_names[:10])
        for sh in xls.sheet_names[:2]:
            df = pd.read_excel(xls, sheet_name=sh, header=None, nrows=18)
            print(f"  --- sheet '{sh}' shape~ {df.shape}")
            for i,row in df.iterrows():
                cells=[("" if pd.isna(v) else str(v))[:16] for v in row.tolist()[:9]]
                print(f"   r{i}:", " | ".join(cells))
    except Exception as e:
        print("  ERR", type(e).__name__, e)
