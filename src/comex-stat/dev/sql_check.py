import io, duckdb, pyarrow as pa, pyarrow.csv as pacsv
from utils import ensure_ca
from subsets_utils import get
ensure_ca()

def read_csv(url):
    import time
    for _ in range(5):
        try:
            raw = get(url, timeout=(10,300)).content; break
        except Exception as e:
            print("retry", e.__class__.__name__); time.sleep(3)
    else:
        raise SystemExit("give up")
    header = raw.split(b"\n",1)[0].decode("utf-8").replace('"','').strip()
    cols=[c for c in header.split(";") if c]
    return pacsv.read_csv(io.BytesIO(raw),
      read_options=pacsv.ReadOptions(encoding="utf-8"),
      parse_options=pacsv.ParseOptions(delimiter=";"),
      convert_options=pacsv.ConvertOptions(column_types={c:pa.string() for c in cols}, strings_can_be_null=True))

con = duckdb.connect()

# exports-ncm transform (1 year)
exp = read_csv("https://balanca.economia.gov.br/balanca/bd/comexstat-bd/ncm/EXP_1998.csv")
con.register("comex-stat-exports-ncm", exp)
r = con.execute('''SELECT CAST(CO_ANO AS INTEGER) AS year, CAST(CO_MES AS INTEGER) AS month,
  CO_NCM AS ncm_code, CO_UNID AS unit_code, CO_PAIS AS country_code, SG_UF_NCM AS state,
  CO_VIA AS transport_mode_code, CO_URF AS customs_code,
  TRY_CAST(QT_ESTAT AS BIGINT) AS statistical_quantity, TRY_CAST(KG_LIQUIDO AS BIGINT) AS net_weight_kg,
  TRY_CAST(VL_FOB AS BIGINT) AS fob_value_usd FROM "comex-stat-exports-ncm" WHERE CO_ANO IS NOT NULL''').arrow()
print("exports-ncm rows", r.num_rows, "cols", r.column_names)
print(r.slice(0,2).to_pylist())

# pais transform
pais = read_csv("https://balanca.economia.gov.br/balanca/bd/tabelas/PAIS.csv")
con.register("comex-stat-pais", pais)
rp = con.execute('''SELECT CO_PAIS AS country_code, CO_PAIS_ISON3 AS iso_numeric_code,
  CO_PAIS_ISOA3 AS iso_alpha3_code, NO_PAIS AS name_pt, NO_PAIS_ING AS name_en, NO_PAIS_ESP AS name_es
  FROM "comex-stat-pais" WHERE CO_PAIS IS NOT NULL''').arrow()
print("pais rows", rp.num_rows, "uniq", len(set(pais.column("CO_PAIS").to_pylist())))
# uf_mun
um = read_csv("https://balanca.economia.gov.br/balanca/bd/tabelas/UF_MUN.csv")
print("uf_mun rows", um.num_rows, "cols", um.column_names)
# ncm uniqueness
ncm = read_csv("https://balanca.economia.gov.br/balanca/bd/tabelas/NCM.csv")
vals = ncm.column("CO_NCM").to_pylist()
print("ncm rows", ncm.num_rows, "uniq", len(set(vals)))
