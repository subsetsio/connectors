"""npm-daily-downloads — trailing-365-day daily download counts (long format).

downloads/range is pulled as a fixed trailing 365-day window
(overwrite -> rolling year).
"""
from datetime import datetime, timedelta, timezone
from urllib.parse import quote

import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet

from utils import _get_json, _get_resp, _popular_names

DOWNLOADS_RANGE = "https://api.npmjs.org/downloads/range"
DOWNLOAD_BULK_SIZE = 128    # downloads/range bulk cap (non-scoped only)
RANGE_DAYS = 365            # downloads/range max window

_DOWNLOADS_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("date", pa.string()),
    ("downloads", pa.int64()),
])


def _parse_downloads(data: dict) -> list[dict]:
    rows = []
    # Single-package shape vs bulk {pkg: {...}} shape.
    if "package" in data and "downloads" in data:
        pkg = data["package"]
        for day in data.get("downloads") or []:
            rows.append({"package": pkg, "date": day["day"], "downloads": int(day["downloads"])})
    else:
        for pkg, pdata in data.items():
            if not pdata:
                continue
            for day in pdata.get("downloads") or []:
                rows.append({"package": pkg, "date": day["day"], "downloads": int(day["downloads"])})
    return rows


def fetch_daily_downloads(node_id: str) -> None:
    names = _popular_names()
    end = (datetime.now(timezone.utc) - timedelta(days=2)).strftime("%Y-%m-%d")
    start = (datetime.now(timezone.utc) - timedelta(days=RANGE_DAYS)).strftime("%Y-%m-%d")
    rng = f"{start}:{end}"
    print(f"  {node_id}: {len(names):,} packages over {rng}")

    non_scoped = [n for n in names if not n.startswith("@")]
    scoped = [n for n in names if n.startswith("@")]

    rows: list[dict] = []
    for i in range(0, len(non_scoped), DOWNLOAD_BULK_SIZE):
        batch = non_scoped[i:i + DOWNLOAD_BULK_SIZE]
        data = _get_json(f"{DOWNLOADS_RANGE}/{rng}/{','.join(batch)}")
        rows.extend(_parse_downloads(data))

    # Scoped packages are unsupported by the bulk form — fetch individually.
    for n in scoped:
        resp = _get_resp(f"{DOWNLOADS_RANGE}/{rng}/{quote(n, safe='@/')}")
        if resp is not None:
            rows.extend(_parse_downloads(resp.json()))

    table = pa.Table.from_pylist(rows, schema=_DOWNLOADS_SCHEMA)
    save_raw_parquet(table, node_id)
    print(f"  {node_id}: {table.num_rows:,} download rows")


DOWNLOAD_SPECS = []

TRANSFORM_SPECS = []
