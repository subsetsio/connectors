"""sec-facts — long-format cross-company financial values from the XBRL Frames
API (one concept across all filers per period), iterated over the curated
concept set x all available periods.

Written as one parquet batch per concept (asset id sec-facts-<tag>-<unit>); the
transform's "sec-facts" view glob-unions all batches. Periods with no data
(future quarters, early years) return 404 and are skipped.
"""
import pyarrow as pa

from subsets_utils import configure_http, save_raw_parquet
from utils import CONCEPTS, USER_AGENT, periods_for, try_frame

FACTS_SCHEMA = pa.schema([
    ("cik", pa.int64()),
    ("entity_name", pa.string()),
    ("taxonomy", pa.string()),
    ("tag", pa.string()),
    ("unit", pa.string()),
    ("fiscal_year", pa.int32()),
    ("fiscal_period", pa.string()),
    ("period_start", pa.string()),   # ISO date or null (instant has no start)
    ("period_end", pa.string()),     # ISO date
    ("value", pa.float64()),
    ("accession", pa.string()),
    ("loc", pa.string()),
])


def fetch_facts(node_id: str) -> None:
    configure_http(headers={"User-Agent": USER_AGENT})
    for taxonomy, tag, unit, ctype in CONCEPTS:
        rows = []
        for period in periods_for(ctype):
            data = try_frame(taxonomy, tag, unit, period)
            if not data:
                continue
            year = int(period[2:6])
            for d in data.get("data", []):
                rows.append({
                    "cik": d.get("cik"),
                    "entity_name": d.get("entityName"),
                    "taxonomy": taxonomy,
                    "tag": tag,
                    "unit": unit,
                    "fiscal_year": year,
                    "fiscal_period": period,
                    "period_start": d.get("start"),
                    "period_end": d.get("end"),
                    "value": d.get("val"),
                    "accession": d.get("accn"),
                    "loc": d.get("loc"),
                })
        if not rows:
            print(f"  no Frames data for {tag}/{unit}; skipping batch")
            continue
        table = pa.Table.from_pylist(rows, schema=FACTS_SCHEMA)
        batch_key = f"{tag.lower()}-{unit.lower()}"
        save_raw_parquet(table, f"sec-facts-{batch_key}")
