"""popular_packages — bulk ranking + per-package metadata (concurrent).

The top ``N_META`` projects by 30-day downloads, each enriched with metadata
from the official PyPI JSON API (pypi.org/pypi/{package}/json). One row per
package. PyPI's Fastly CDN has no observed rate limit, so metadata is fetched
concurrently.

Scope is deliberately top-N (popularity ranked): the top 5,000 projects cover
~95% of total PyPI download volume. This is a stateless full re-pull — the bulk
file is a fresh monthly snapshot and the PyPI JSON API has no incremental filter
— so there is no watermark to carry. Raw is written with every column as a
string (a stable cross-run contract); all typing/casting is deferred to the SQL
transform, the correctness gate.
"""

import concurrent.futures as cf

import httpx
import pyarrow as pa

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_parquet
from utils import get_json, load_universe, s

PYPI_JSON_URL = "https://pypi.org/pypi/{package}/json"

# Popularity-ranked scope cap (see module docstring). The top 5,000 projects
# cover ~95% of total PyPI download volume.
N_META = 5000

_META_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("rank", pa.string()),
    ("download_count_30d", pa.string()),
    ("version", pa.string()),
    ("summary", pa.string()),
    ("author", pa.string()),
    ("author_email", pa.string()),
    ("license", pa.string()),
    ("requires_python", pa.string()),
    ("home_page", pa.string()),
    ("keywords", pa.string()),
    ("yanked", pa.string()),
])


def _fetch_meta(package: str) -> dict:
    """Metadata for one package from the PyPI JSON API. A 404 (package gone /
    renamed) is permanent — return empty metadata rather than failing the node."""
    try:
        info = get_json(PYPI_JSON_URL.format(package=package)).get("info", {})
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return {}
        raise
    return {
        "version": info.get("version"),
        "summary": info.get("summary") or None,
        "author": info.get("author") or None,
        "author_email": info.get("author_email") or None,
        # PyPI is migrating from the free-text `license` to the SPDX
        # `license_expression`; prefer the latter when present.
        "license": info.get("license_expression") or info.get("license") or None,
        "requires_python": info.get("requires_python") or None,
        "home_page": info.get("home_page") or None,
        "keywords": info.get("keywords") or None,
        "yanked": info.get("yanked"),
    }


def fetch_popular_packages(node_id: str) -> None:
    asset = node_id
    universe = load_universe()[:N_META]
    names = [r["project"] for r in universe]
    downloads = {r["project"]: r.get("download_count") for r in universe}
    print(f"  {asset}: fetching metadata for {len(names)} packages...")

    meta_by_name: dict[str, dict] = {}
    with cf.ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(_fetch_meta, n): n for n in names}
        done = 0
        for fut in cf.as_completed(futures):
            name = futures[fut]
            meta_by_name[name] = fut.result()  # transient already retried; bugs raise
            done += 1
            if done % 1000 == 0:
                print(f"    [{done}/{len(names)}] metadata fetched")

    rows = []
    for rank, name in enumerate(names, start=1):
        m = meta_by_name.get(name, {})
        rows.append({
            "package": name,
            "rank": str(rank),
            "download_count_30d": s(downloads.get(name)),
            "version": s(m.get("version")),
            "summary": s(m.get("summary")),
            "author": s(m.get("author")),
            "author_email": s(m.get("author_email")),
            "license": s(m.get("license")),
            "requires_python": s(m.get("requires_python")),
            "home_page": s(m.get("home_page")),
            "keywords": s(m.get("keywords")),
            "yanked": s(m.get("yanked")),
        })

    table = pa.Table.from_pylist(rows, schema=_META_SCHEMA)
    print(f"  {asset}: {table.num_rows:,} packages")
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="pypi-popular-packages", fn=fetch_popular_packages, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="pypi-popular-packages-transform",
        deps=["pypi-popular-packages"],
        sql='''
            SELECT
                package,
                CAST(rank AS INTEGER)               AS rank,
                CAST(download_count_30d AS BIGINT)  AS download_count_30d,
                version,
                summary,
                author,
                author_email,
                license,
                requires_python,
                home_page,
                keywords,
                CAST(yanked AS BOOLEAN)             AS yanked
            FROM "pypi-popular-packages"
            WHERE package IS NOT NULL
        ''',
    ),
]
