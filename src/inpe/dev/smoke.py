import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))
import nodes.inpe as m
import constants as C

# Limit each directory listing to a single recent year to keep the smoke test fast.
_orig = m._list_zip_urls
def one_year(dir_url):
    urls = _orig(dir_url)
    return [u for u in urls if "2023" in u] or urls[-1:]
m._list_zip_urls = one_year

# Capture saved tables instead of writing to the raw layer.
saved = {}
def fake_save(table, asset):
    saved[asset] = table
    print(f"[{asset}] rows={table.num_rows} cols={table.column_names}")
m.save_raw_parquet = fake_save

for fn, nid in [
    (m.fetch_estado_mensal, "inpe-focos-brasil-estado-mensal"),
    (m.fetch_bioma_mensal, "inpe-focos-brasil-bioma-mensal"),
    (m.fetch_municipio_anual, "inpe-focos-brasil-municipio-anual"),
    (m.fetch_brasil_mensal, "inpe-focos-brasil-mensal"),
    (m.fetch_america_sul_pais_mensal, "inpe-focos-america-sul-pais-mensal"),
]:
    fn(nid)
    t = saved[nid]
    print("  sample:", t.slice(0, 3).to_pylist())
    print("  n_focos total:", __import__("pyarrow.compute", fromlist=["sum"]).sum(t["n_focos"]).as_py())
