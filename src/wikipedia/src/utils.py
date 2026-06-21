"""Shared HTTP + parse helpers for the Wikipedia AQS connector.

Holds the no-auth Wikimedia Analytics Query Service (AQS) client, the live
project-universe discovery, and the per-project collect engine used by every
metric family. Node files import these as `from utils import ...`; this module
contains NO NodeSpec definitions.
"""
from datetime import datetime, timezone

import httpx
import pyarrow as pa
from ratelimit import limits, sleep_and_retry

from subsets_utils import get, save_raw_parquet, transient_retry

# ASCII-only User-Agent (mandatory per AQS policy; plain hyphens only).
_HEADERS = {
    "User-Agent": "subsets.io-wikipedia-connector/1.0 (https://subsets.io; nathan@subsets.io)"
}
BASE = "https://wikimedia.org/api/rest_v1/metrics"
# AQS only 404s a request whose whole range predates the data; a range ending
# now always spans each family's true start, so one early start works for all.
START = "2001010100"
# Catastrophic-break floor: if a per-project family returns data for fewer than
# this many projects, sitematrix or the API degraded — fail loudly.
_MIN_PROJECTS = 100


@sleep_and_retry
@limits(calls=4, period=1)  # ~4 req/s/process; aggregate across specs stays well under AQS caps
def _rate_limited_get(url: str) -> httpx.Response:
    return get(url, headers=_HEADERS, timeout=(10.0, 120.0))


@transient_retry()
def get_json(url: str):
    resp = _rate_limited_get(url)
    resp.raise_for_status()
    return resp.json()


def now_end() -> str:
    # End at the current day; AQS returns through the latest complete month.
    return datetime.now(tz=timezone.utc).strftime("%Y%m%d") + "00"


def to_date(ts) -> str:
    """Normalize AQS timestamps to 'YYYY-MM-DD'.

    Two shapes occur: flat-item families echo 'YYYYMMDD[HH]'; nested-results
    families use ISO-8601 ('2024-01-01T00:00:00.000Z').
    """
    s = str(ts)
    if "T" in s:
        return s[:10]
    d = s[:8]
    return f"{d[0:4]}-{d[4:6]}-{d[6:8]}"


def projects() -> list[str]:
    """Live list of Wikimedia project hostnames from the sitematrix."""
    data = get_json(
        "https://www.wikidata.org/w/api.php?action=sitematrix&format=json"
        "&smstate=all&maxlag=5"
    )
    sm = data["sitematrix"]
    hosts: list[str] = ["all-projects"]
    seen = {"all-projects"}
    groups = list(sm.values()) + [{"site": sm.get("specials", [])}]
    for grp in groups:
        if not isinstance(grp, dict):
            continue
        for site in grp.get("site", []):
            url = site.get("url", "")
            if not url.startswith("https://"):
                continue
            host = url[len("https://"):].rstrip("/")
            if host and host not in seen:
                seen.add(host)
                hosts.append(host)
    return hosts


def collect_per_project(node_id: str, path_for, parse_into, schema: pa.Schema) -> None:
    """Loop the project universe, fetch each project's series, write one parquet.

    `path_for(project)` builds the URL; `parse_into(data, rows)` appends row
    dicts from one project's JSON response (it reads the canonical project code
    the API echoes, so callers needn't pass it back).
    """
    rows: list[dict] = []
    ok = 0
    for project in projects():
        url = path_for(project)
        try:
            data = get_json(url)
        except httpx.HTTPStatusError as e:
            code = e.response.status_code
            # 404 = no data for this project; other 4xx (not 429) = bad project
            # code. Either way skip this project and keep going.
            if code != 429 and 400 <= code < 500:
                continue
            raise
        before = len(rows)
        parse_into(data, rows)
        if len(rows) > before:
            ok += 1
    if ok < _MIN_PROJECTS:
        raise RuntimeError(
            f"{node_id}: only {ok} projects returned data (floor {_MIN_PROJECTS}); "
            "sitematrix or AQS likely degraded"
        )
    table = pa.Table.from_pylist(rows, schema=schema)
    save_raw_parquet(table, node_id)


def parse_nested(value_key):
    def parse_into(data, rows):
        for it in data.get("items", []):
            project = it.get("project")
            for r in it.get("results", []):
                rows.append({
                    "project": project,
                    "date": to_date(r["timestamp"]),
                    value_key: r.get(value_key),
                })
    return parse_into


def per_project_sql(spec_id: str, value_cols: list[str]) -> str:
    # Quote column names — some (e.g. "offset") are DuckDB reserved keywords.
    primary = f'"{value_cols[0]}"'
    cols = ", ".join(f'"{c}"' for c in value_cols)
    return f'''
        SELECT
            project,
            CAST(date AS DATE) AS date,
            {cols}
        FROM "{spec_id}"
        WHERE project IS NOT NULL
          AND date IS NOT NULL
          AND {primary} IS NOT NULL
    '''
