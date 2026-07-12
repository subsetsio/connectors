"""CRAN download-logs connector.

Three published subsets, all sourced from the aggregated cranlogs REST API
(https://cranlogs.r-pkg.org) plus the crandb package catalog
(https://crandb.r-pkg.org):

- packages          : reference catalog of all CRAN packages (crandb /-/latest).
- package_downloads : long-format daily download counts per package per day.
                      ~24k packages fetched in batches of 100 from the cranlogs
                      daily endpoint over the full history (2012-10-01 -> today),
                      streamed to a single parquet asset.
- r_downloads       : daily R-language downloads broken down by OS and version
                      (cranlogs special package name "R").

Fetch shape: stateless full re-pull every run (the aggregated API restates the
whole history cheaply; ~240 batched requests, ~20 min). Revisions/late
corrections are picked up for free because no watermark is trusted.
"""

from datetime import datetime, timezone

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

CRANLOGS = "https://cranlogs.r-pkg.org"
CRANDB = "https://crandb.r-pkg.org"
HISTORY_START = "2012-10-01"  # first day the RStudio mirror published logs
PKG_BATCH = 100               # packages per cranlogs request (URL-length safe)

PACKAGES_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("version", pa.string()),
    ("title", pa.string()),
    ("description", pa.string()),
    ("license", pa.string()),
    ("maintainer", pa.string()),
    ("needs_compilation", pa.string()),
    ("date_publication", pa.string()),
    ("url", pa.string()),
    ("bugreports", pa.string()),
    ("repository", pa.string()),
])

PKG_DOWNLOADS_SCHEMA = pa.schema([
    ("package", pa.string()),
    ("day", pa.string()),
    ("downloads", pa.int64()),
])

R_DOWNLOADS_SCHEMA = pa.schema([
    ("day", pa.string()),
    ("os", pa.string()),
    ("version", pa.string()),
    ("downloads", pa.int64()),
])


@transient_retry()
def _get_json(url, timeout=(15.0, 300.0)):
    resp = get(url, timeout=timeout)
    resp.raise_for_status()
    return resp.json()


def _today():
    return datetime.now(tz=timezone.utc).date().isoformat()


def _s(value):
    """Coerce a crandb field to a plain string (or None)."""
    if value is None:
        return None
    if isinstance(value, str):
        return value
    return str(value)


def fetch_packages(node_id: str) -> None:
    asset = node_id
    catalog = _get_json(f"{CRANDB}/-/latest")
    rows = []
    for name, rec in catalog.items():
        rows.append({
            "package": _s(rec.get("Package")) or name,
            "version": _s(rec.get("Version")),
            "title": _s(rec.get("Title")),
            "description": _s(rec.get("Description")),
            "license": _s(rec.get("License")),
            "maintainer": _s(rec.get("Maintainer")),
            "needs_compilation": _s(rec.get("NeedsCompilation")),
            "date_publication": _s(rec.get("Date/Publication")),
            "url": _s(rec.get("URL")),
            "bugreports": _s(rec.get("BugReports")),
            "repository": _s(rec.get("Repository")),
        })
    table = pa.Table.from_pylist(rows, schema=PACKAGES_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_r_downloads(node_id: str) -> None:
    asset = node_id
    end = _today()
    data = _get_json(f"{CRANLOGS}/downloads/daily/{HISTORY_START}:{end}/R")
    rows = []
    for obj in data:
        for d in (obj.get("downloads") or []):
            rows.append({
                "day": d.get("day"),
                "os": d.get("os"),
                "version": d.get("version"),
                "downloads": int(d["downloads"]) if d.get("downloads") is not None else None,
            })
    if not rows:
        raise AssertionError("R downloads returned no records")
    table = pa.Table.from_pylist(rows, schema=R_DOWNLOADS_SCHEMA)
    save_raw_parquet(table, asset)


def fetch_package_downloads(node_id: str) -> None:
    asset = node_id
    end = _today()
    # All current CRAN package names, sorted for stable batch boundaries.
    desc = _get_json(f"{CRANDB}/-/desc")
    names = sorted(desc.keys())
    if len(names) < 15000:
        raise AssertionError(
            f"crandb returned only {len(names)} packages; expected ~24k "
            "(catalog fetch likely degraded)"
        )

    with raw_parquet_writer(asset, PKG_DOWNLOADS_SCHEMA) as writer:
        for start in range(0, len(names), PKG_BATCH):
            batch = names[start:start + PKG_BATCH]
            url = f"{CRANLOGS}/downloads/daily/{HISTORY_START}:{end}/" + ",".join(batch)
            data = _get_json(url)
            rows = []
            for obj in data:
                pkg = obj.get("package")
                for d in (obj.get("downloads") or []):
                    cnt = d.get("downloads")
                    if cnt is None:
                        continue
                    rows.append({
                        "package": pkg,
                        "day": d.get("day"),
                        "downloads": int(cnt),
                    })
            if rows:
                writer.write_table(pa.Table.from_pylist(rows, schema=PKG_DOWNLOADS_SCHEMA))


DOWNLOAD_SPECS = [
    NodeSpec(id="cran-logs-packages", fn=fetch_packages, kind="download"),
    NodeSpec(id="cran-logs-package-downloads", fn=fetch_package_downloads, kind="download"),
    NodeSpec(id="cran-logs-r-downloads", fn=fetch_r_downloads, kind="download"),
]
