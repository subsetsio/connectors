"""Download nodes for the PyPI connector."""

from __future__ import annotations

import concurrent.futures as cf

import httpx
import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get,
    raw_asset_exists,
    record_source_signature,
    save_raw_parquet,
    source_unchanged,
)

TOP_PACKAGES_URL = (
    "https://hugovk.github.io/top-pypi-packages/top-pypi-packages-30-days.min.json"
)
PYPI_JSON_URL = "https://pypi.org/pypi/{package}/json"

_SCHEMA = pa.schema(
    [
        ("package", pa.string()),
        ("rank", pa.int64()),
        ("download_count_30d", pa.int64()),
        ("snapshot_last_update", pa.string()),
        ("version", pa.string()),
        ("summary", pa.string()),
        ("author", pa.string()),
        ("author_email", pa.string()),
        ("license", pa.string()),
        ("license_expression", pa.string()),
        ("requires_python", pa.string()),
        ("home_page", pa.string()),
        ("project_urls", pa.string()),
        ("keywords", pa.string()),
        ("classifiers", pa.string()),
        ("yanked", pa.bool_()),
    ]
)


def _json_get(url: str) -> tuple[dict, httpx.Response]:
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    if not resp.content:
        raise RuntimeError(f"empty response body from {url}")
    return resp.json(), resp


def _scalar(value):
    if value in ("", [], {}, ()):
        return None
    return value


def _join_list(value) -> str | None:
    if not value:
        return None
    if isinstance(value, list):
        return "\n".join(str(item) for item in value)
    return str(value)


def _project_urls(value) -> str | None:
    if not isinstance(value, dict) or not value:
        return None
    return "\n".join(f"{key}: {url}" for key, url in sorted(value.items()))


def _fetch_package_metadata(package: str) -> dict:
    try:
        data, _ = _json_get(PYPI_JSON_URL.format(package=package))
    except httpx.HTTPStatusError as exc:
        if exc.response.status_code == 404:
            return {}
        raise
    info = data.get("info") or {}
    return {
        "version": _scalar(info.get("version")),
        "summary": _scalar(info.get("summary")),
        "author": _scalar(info.get("author")),
        "author_email": _scalar(info.get("author_email")),
        "license": _scalar(info.get("license")),
        "license_expression": _scalar(info.get("license_expression")),
        "requires_python": _scalar(info.get("requires_python")),
        "home_page": _scalar(info.get("home_page")),
        "project_urls": _project_urls(info.get("project_urls")),
        "keywords": _scalar(info.get("keywords")),
        "classifiers": _join_list(info.get("classifiers")),
        "yanked": bool(info.get("yanked") or False),
    }


def fetch_popular_packages(node_id: str) -> None:
    top_data, response = _json_get(TOP_PACKAGES_URL)
    rows = top_data.get("rows") or []
    if not rows:
        raise RuntimeError("top PyPI packages response had no rows")

    rows = sorted(rows, key=lambda row: row.get("download_count") or 0, reverse=True)
    package_names = [str(row["project"]) for row in rows if row.get("project")]
    download_counts = {
        str(row["project"]): int(row.get("download_count") or 0)
        for row in rows
        if row.get("project")
    }
    snapshot_last_update = top_data.get("last_update")

    metadata_by_package: dict[str, dict] = {}
    with cf.ThreadPoolExecutor(max_workers=16) as pool:
        futures = {pool.submit(_fetch_package_metadata, package): package for package in package_names}
        completed = 0
        for future in cf.as_completed(futures):
            package = futures[future]
            metadata_by_package[package] = future.result()
            completed += 1
            if completed % 1000 == 0:
                print(f"{node_id}: fetched metadata for {completed}/{len(package_names)} packages")

    table_rows = []
    for rank, package in enumerate(package_names, start=1):
        metadata = metadata_by_package.get(package) or {}
        table_rows.append(
            {
                "package": package,
                "rank": rank,
                "download_count_30d": download_counts.get(package, 0),
                "snapshot_last_update": snapshot_last_update,
                "version": metadata.get("version"),
                "summary": metadata.get("summary"),
                "author": metadata.get("author"),
                "author_email": metadata.get("author_email"),
                "license": metadata.get("license"),
                "license_expression": metadata.get("license_expression"),
                "requires_python": metadata.get("requires_python"),
                "home_page": metadata.get("home_page"),
                "project_urls": metadata.get("project_urls"),
                "keywords": metadata.get("keywords"),
                "classifiers": metadata.get("classifiers"),
                "yanked": metadata.get("yanked", False),
            }
        )

    save_raw_parquet(pa.Table.from_pylist(table_rows, schema=_SCHEMA), node_id)
    record_source_signature(node_id, TOP_PACKAGES_URL, response=response)


DOWNLOAD_SPECS = [
    NodeSpec(id="pypi-popular-packages", fn=fetch_popular_packages),
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="pypi-popular-packages",
        description=(
            "Updated monthly by hugovk/top-pypi-packages; use source HTTP "
            "ETag/Last-Modified signature from the top-packages JSON."
        ),
        check=lambda asset_id: source_unchanged(asset_id, TOP_PACKAGES_URL)
        and raw_asset_exists(asset_id, "parquet"),
    ),
]
