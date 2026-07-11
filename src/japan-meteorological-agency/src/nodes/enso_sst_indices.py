"""TCC: ENSO / SST monitoring indices."""
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_parquet
from utils import TCC

# ENSO/SST monitoring products: (region, measure, url). region+measure are
# columns on one long-format table — this fixed set IS the product catalog, not
# a hardcoded year range (years are discovered from each file's rows).
_ENSO_PRODUCTS = [
    ("NINO.1+2", "sst",     f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_1+2/sst"),
    ("NINO.1+2", "anomaly", f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_1+2/anomaly"),
    ("NINO.3",   "sst",     f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_3/sst"),
    ("NINO.3",   "anomaly", f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_3/anomaly"),
    ("NINO.4",   "sst",     f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_4/sst"),
    ("NINO.4",   "anomaly", f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_4/anomaly"),
    ("NINO.WEST", "sst",     f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_West/sst"),
    ("NINO.WEST", "anomaly", f"{TCC}/elnino/index/sstindex/base_period_9120/Nino_West/anomaly"),
    ("IOBW",     "sst",     f"{TCC}/elnino/index/sstindex/sliding_30year_period/IOBW/sst"),
    ("IOBW",     "anomaly", f"{TCC}/elnino/index/sstindex/sliding_30year_period/IOBW/deviation"),
]

_MISSING = {99.9, 99.90, 999.9}  # TCC fill value for not-yet-observed months

_ENSO_SCHEMA = pa.schema([
    ("region", pa.string()),
    ("measure", pa.string()),
    ("year", pa.int64()),
    ("month", pa.int64()),
    ("value", pa.float64()),
])


def fetch_enso_sst_indices(node_id: str) -> None:
    rows = []
    for region, measure, url in _ENSO_PRODUCTS:
        text = get(url, timeout=60).text
        lines = text.splitlines()
        for line in lines[1:]:  # first line is the month header
            parts = line.split()
            if len(parts) < 2:
                continue
            try:
                year = int(parts[0])
            except ValueError:
                continue
            for month, raw in enumerate(parts[1:13], start=1):
                try:
                    val = float(raw)
                except ValueError:
                    continue
                if val in _MISSING:
                    continue
                rows.append({
                    "region": region,
                    "measure": measure,
                    "year": year,
                    "month": month,
                    "value": val,
                })
    if not rows:
        raise RuntimeError("ENSO/SST products parsed to 0 rows")
    save_raw_parquet(pa.Table.from_pylist(rows, schema=_ENSO_SCHEMA), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="japan-meteorological-agency-enso-sst-indices", fn=fetch_enso_sst_indices, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="japan-meteorological-agency-enso-sst-indices-transform",
        deps=["japan-meteorological-agency-enso-sst-indices"],
        sql='''
            SELECT
                region, measure,
                make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
                year, month, value
            FROM "japan-meteorological-agency-enso-sst-indices"
            WHERE value IS NOT NULL
            ORDER BY region, measure, year, month
        ''',
    ),
]
