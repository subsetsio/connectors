"""download_trends — per-package daily series from pypistats (rate-limited).

A long-format daily download time series for the top ``N_TRENDS`` projects, from
pypistats.org (/api/packages/{pkg}/overall). Columns: package, category
(with_mirrors / without_mirrors), date, downloads. One row per package x
category x day. pypistats only exposes the most recent ~180 days of DAILY data
and is rate-limited (~30 rpm, aggressive HTML 429s), so this node fetches
sequentially with backoff.

This is a stateless full re-pull — pypistats always returns its fixed sliding
180-day window — so there is no watermark to carry. Raw is written with every
column as a string (a stable cross-run contract); all typing/casting is deferred
to the SQL transform, the correctness gate.
"""

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import get_json, load_universe, s

PYPISTATS_URL = "https://pypistats.org/api/packages/{package}/overall"

# Popularity-ranked scope cap. The top 1,000 give a rich daily download panel
# without pushing the rate-limited pypistats crawl past the CI budget
# (~30 rpm => ~1,000 packages in ~35 min).
N_TRENDS = 1000

# pypistats per-package fetch may legitimately fail for a few packages (renamed,
# unicode-normalised, or simply absent from the stats backend). Tolerate a small
# fraction of skips; a larger share means the API itself is degraded -> raise.
MAX_TRENDS_SKIP_FRACTION = 0.10

_TRENDS_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("category", pa.string()),
    ("date", pa.string()),
    ("downloads", pa.string()),
])


def _fetch_trends(package: str):
    """Daily download rows for one package. Returns [] on a permanent 404
    (package absent from the stats backend)."""
    try:
        data = get_json(PYPISTATS_URL.format(package=package))
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return []
        raise
    out = []
    for row in data.get("data", []):
        out.append({
            "package": package,
            "category": row.get("category"),
            "date": row.get("date"),
            "downloads": s(row.get("downloads")),
        })
    return out


def fetch_download_trends(node_id: str) -> None:
    asset = node_id
    names = [r["project"] for r in load_universe()[:N_TRENDS]]
    print(f"  {asset}: fetching daily download series for {len(names)} packages...")

    rows = []
    skipped = []
    for i, name in enumerate(names, start=1):
        try:
            pkg_rows = _fetch_trends(name)
        except Exception as exc:  # transient retries already exhausted
            print(f"  {asset}: {name}: giving up ({type(exc).__name__}: {exc})")
            skipped.append(name)
            continue
        if not pkg_rows:
            skipped.append(name)
        else:
            rows.extend(pkg_rows)
        if i % 200 == 0:
            print(f"    [{i}/{len(names)}] {len(rows):,} rows, {len(skipped)} skipped")

    if len(skipped) > MAX_TRENDS_SKIP_FRACTION * len(names):
        raise RuntimeError(
            f"{asset}: {len(skipped)}/{len(names)} packages failed/empty — "
            "pypistats likely degraded, refusing to publish a partial panel"
        )

    table = pa.Table.from_pylist(rows, schema=_TRENDS_SCHEMA)
    print(f"  {asset}: {table.num_rows:,} rows across "
          f"{len(names) - len(skipped)} packages ({len(skipped)} skipped)")
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="pypi-download-trends", fn=fetch_download_trends, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="pypi-download-trends-transform",
        deps=["pypi-download-trends"],
        sql='''
            SELECT
                package,
                category,
                CAST(date AS DATE)        AS date,
                CAST(downloads AS BIGINT) AS downloads
            FROM "pypi-download-trends"
            WHERE package IS NOT NULL
              AND date IS NOT NULL
              AND downloads IS NOT NULL
        ''',
    ),
]
