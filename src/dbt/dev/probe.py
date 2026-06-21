import io
import pyarrow.parquet as pq
from subsets_utils import get

BASE = "https://data.api.trade.gov.uk"

# (dataset, kind, id)
TARGETS = [
    ("market-barriers", "table", "barriers"),
    ("orp-regulations", "table", "uk-regulatory-documents"),
    ("uk-tariff-2021-01-01", "table", "commodities"),
    ("uk-tariff-2021-01-01", "table", "measures"),
    ("uk-tariff-2021-01-01", "table", "measures-as-defined"),
    ("uk-tariff-2021-01-01", "table", "measures-on-declarable-commodities"),
    ("uk-tariff-2021-01-01", "report", "measures-on-declarable-commodities"),
    ("uk-trade-quotas", "table", "quotas"),
    ("uk-trade-quotas", "report", "quotas-including-current-volumes"),
]

for dataset, kind, tid in TARGETS:
    seg = "tables" if kind == "table" else "reports"
    url = f"{BASE}/v1/datasets/{dataset}/versions/latest/{seg}/{tid}/data"
    try:
        resp = get(url, params={"format": "parquet"}, timeout=(10.0, 120.0))
        resp.raise_for_status()
        t = pq.read_table(io.BytesIO(resp.content))
        print(f"\n=== {dataset}/{kind}/{tid}  rows={t.num_rows} status={resp.status_code} ===")
        for f in t.schema:
            print(f"   {f.name}: {f.type}")
    except Exception as e:
        print(f"\n!!! {dataset}/{kind}/{tid}: {type(e).__name__}: {e}")
