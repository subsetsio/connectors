"""PyPI Stats package download aggregates."""

from __future__ import annotations

import datetime as dt
import time

import pyarrow as pa

from subsets_utils import MaintainSpec, NodeSpec, get, raw_asset_exists, save_raw_parquet


BASE_URL = "https://pypistats.org/api/packages"

TOP_PACKAGES = [
    "boto3",
    "packaging",
    "typing-extensions",
    "certifi",
    "urllib3",
    "requests",
    "idna",
    "charset-normalizer",
    "setuptools",
    "cryptography",
    "botocore",
    "aiobotocore",
    "pluggy",
    "pygments",
    "cffi",
    "python-dateutil",
    "six",
    "pycparser",
    "pyyaml",
    "numpy",
    "pydantic",
]

ENDPOINTS = {
    "pypi-stats-recent-downloads": "recent",
    "pypi-stats-overall-downloads": "overall",
    "pypi-stats-python-major-downloads": "python_major",
    "pypi-stats-python-minor-downloads": "python_minor",
    "pypi-stats-system-downloads": "system",
}

RECENT_SCHEMA = pa.schema(
    [
        ("package", pa.string()),
        ("period", pa.string()),
        ("downloads", pa.int64()),
        ("fetched_at", pa.timestamp("us", tz="UTC")),
    ]
)

TIMESERIES_SCHEMA = pa.schema(
    [
        ("package", pa.string()),
        ("metric", pa.string()),
        ("category", pa.string()),
        ("date", pa.date32()),
        ("downloads", pa.int64()),
        ("fetched_at", pa.timestamp("us", tz="UTC")),
    ]
)


def _fetch_json(package: str, endpoint: str) -> dict:
    url = f"{BASE_URL}/{package}/{endpoint}"
    response = get(url, timeout=(10.0, 120.0))
    response.raise_for_status()
    return response.json()


def _fetch_recent(node_id: str) -> None:
    fetched_at = dt.datetime.now(dt.UTC)
    rows = []
    for package in TOP_PACKAGES:
        payload = _fetch_json(package, "recent")
        data = payload.get("data") or {}
        for period in ("last_day", "last_week", "last_month"):
            value = data.get(period)
            if value is not None:
                rows.append(
                    {
                        "package": package,
                        "period": period,
                        "downloads": int(value),
                        "fetched_at": fetched_at,
                    }
                )
        time.sleep(0.1)
    save_raw_parquet(pa.Table.from_pylist(rows, schema=RECENT_SCHEMA), node_id)


def _fetch_timeseries(node_id: str, endpoint: str) -> None:
    fetched_at = dt.datetime.now(dt.UTC)
    rows = []
    for package in TOP_PACKAGES:
        payload = _fetch_json(package, endpoint)
        for item in payload.get("data") or []:
            rows.append(
                {
                    "package": package,
                    "metric": payload.get("type") or endpoint,
                    "category": item.get("category"),
                    "date": dt.date.fromisoformat(item["date"]),
                    "downloads": int(item["downloads"]),
                    "fetched_at": fetched_at,
                }
            )
        time.sleep(0.1)
    save_raw_parquet(pa.Table.from_pylist(rows, schema=TIMESERIES_SCHEMA), node_id)


def fetch_downloads(node_id: str) -> None:
    endpoint = ENDPOINTS[node_id]
    if endpoint == "recent":
        _fetch_recent(node_id)
    else:
        _fetch_timeseries(node_id, endpoint)


DOWNLOAD_SPECS = [
    NodeSpec(id="pypi-stats-overall-downloads", fn=fetch_downloads, kind="download"),
    NodeSpec(id="pypi-stats-python-major-downloads", fn=fetch_downloads, kind="download"),
    NodeSpec(id="pypi-stats-python-minor-downloads", fn=fetch_downloads, kind="download"),
    NodeSpec(id="pypi-stats-recent-downloads", fn=fetch_downloads, kind="download"),
    NodeSpec(id="pypi-stats-system-downloads", fn=fetch_downloads, kind="download"),
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "PyPI Stats API data is updated once daily per https://pypistats.org/api/; "
            "refresh raw assets after 1 day."
        ),
        check=lambda asset_id: raw_asset_exists(asset_id, "parquet", max_age_days=1),
    )
    for spec in DOWNLOAD_SPECS
]
