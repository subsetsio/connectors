"""npm-package-inventory - live package IDs from the npm replication API.

The CouchDB `_all_docs` endpoint returns current package document IDs without
expensive full packuments. It is the cheapest stable path for a whole-registry
package inventory snapshot.
"""
import json

import pyarrow as pa

from subsets_utils import NodeSpec, raw_parquet_writer

from utils import _get_json

ALL_DOCS_URL = "https://replicate.npmjs.com/registry/_all_docs"
PAGE_SIZE = 10000

_INVENTORY_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("rev", pa.string()),
])


def fetch_package_inventory(node_id: str) -> None:
    params: dict[str, object] = {"limit": PAGE_SIZE}
    last_key: str | None = None
    total = 0
    with raw_parquet_writer(node_id, _INVENTORY_SCHEMA) as writer:
        while True:
            data = _get_json(ALL_DOCS_URL, params=params)
            rows = data.get("rows") or []
            fetched_count = len(rows)
            if last_key is not None:
                rows = [row for row in rows if row.get("key") != last_key]
            if not rows:
                break
            batch = [
                {
                    "package": row.get("id"),
                    "rev": (row.get("value") or {}).get("rev"),
                }
                for row in rows
                if row.get("id")
            ]
            writer.write_table(pa.Table.from_pylist(batch, schema=_INVENTORY_SCHEMA))
            total += len(batch)
            if fetched_count < PAGE_SIZE:
                break
            last_key = rows[-1]["key"]
            params = {
                "limit": PAGE_SIZE,
                "startkey": json.dumps(last_key),
            }
            if total % 250000 == 0:
                print(f"  {node_id}: {total:,} packages")
    print(f"  {node_id}: {total:,} packages")


DOWNLOAD_SPECS = []
