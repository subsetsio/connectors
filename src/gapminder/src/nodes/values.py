"""gapminder-values: long-format observations across every single-geo-by-time
indicator in both repos (geo, time, indicator, value).

Stateless full re-pull (shape 1): each run re-reads each repo's datapackage.json
to enumerate the datapoints CSVs, re-fetches them all (~850 small files, a few
minutes), and overwrites. No watermark/cursor — the source has no incremental
filter, the corpus is small, and a full re-pull picks up late revisions for free.
"""
import csv
import io

import pyarrow as pa

from subsets_utils import raw_parquet_writer
from utils import REPOS, get_json, get_text

# DDF geo-like dimension names that identify a single-entity-by-time datapoints
# resource (exactly one value column). Multidimensional files (extra dims such as
# gender/age) carry a primaryKey with >2 members and are excluded here, since they
# would not fit the (geo, time, value) long-format schema.
GEO_DIMS = {
    "geo", "country", "global", "world_4region", "world_6region",
    "income_groups", "un_sdg_region",
}


def _datapoint_resources(datapackage: dict):
    """Yield (path, geo_dim, indicator) for single-geo-by-time datapoints."""
    for r in datapackage.get("resources", []):
        path = r.get("path", "")
        if "datapoints" not in path:
            continue
        schema = r.get("schema", {})
        pk = schema.get("primaryKey")
        if not isinstance(pk, list) or len(pk) != 2:
            continue
        geo_dim, time_dim = pk[0], pk[1]
        if time_dim != "time" or geo_dim not in GEO_DIMS:
            continue
        fields = [f["name"] for f in schema.get("fields", [])]
        value_cols = [f for f in fields if f not in (geo_dim, "time")]
        if len(value_cols) != 1:
            continue
        yield path, geo_dim, value_cols[0]


VALUES_SCHEMA = pa.schema([
    ("repo", pa.string()),
    ("geo_dim", pa.string()),
    ("geo", pa.string()),
    ("time", pa.string()),
    ("indicator", pa.string()),
    ("value", pa.string()),
])


def fetch_values(node_id: str) -> None:
    asset = node_id
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        for repo, base in REPOS.items():
            dp = get_json(base + "/datapackage.json")
            for path, geo_dim, indicator in _datapoint_resources(dp):
                text = get_text(f"{base}/{path}")
                geos, times, vals = [], [], []
                for row in csv.DictReader(io.StringIO(text)):
                    val = row.get(indicator)
                    if val is None or val == "":
                        continue
                    geos.append(row.get(geo_dim))
                    times.append(row.get("time"))
                    vals.append(val)
                if not geos:
                    continue
                n = len(geos)
                batch = pa.table(
                    {
                        "repo": pa.array([repo] * n, pa.string()),
                        "geo_dim": pa.array([geo_dim] * n, pa.string()),
                        "geo": pa.array(geos, pa.string()),
                        "time": pa.array(times, pa.string()),
                        "indicator": pa.array([indicator] * n, pa.string()),
                        "value": pa.array(vals, pa.string()),
                    },
                    schema=VALUES_SCHEMA,
                )
                writer.write_table(batch)
