"""Common Crawl — per-crawl aggregate statistics.

Source: the immutable crawl-analysis stats files published by Common Crawl,
one gzip per monthly crawl at
`https://data.commoncrawl.org/crawl-analysis/<CRAWL>/stats/part-00000.gz`.
The set of crawls is enumerated from `https://index.commoncrawl.org/collinfo.json`.

Each stats line is `<json-key>\t<value>` where the JSON key is an array whose
first element is the metric family and whose element [2] is the crawl id, e.g.

    ["http_status",200,"CC-MAIN-2026-21"]\t2164140877
    ["languages","eng","CC-MAIN-2026-21"]\t[12345,6789]
    ["histogram","url","CC-MAIN-2026-21","page",100]\t141

The `value` is polymorphic: a scalar page count, or a list whose FIRST element
is the page count (`[pages, urls]`, `[pages, urls, hosts]`, ...), or — for the
`size_estimate` family only — a HyperLogLog cardinality sketch object. We
publish the page count (the one metric present for every family) as a single
long-format table `(crawl_id, crawl_date, metric_family, key, count)`. The two
`size_estimate` rows per crawl are cardinality sketches, not counts, and are
dropped.

Fetch shape: stateless full re-pull. The whole corpus is ~124 small (~1MB gzip)
immutable files, fetched in a few minutes, and cloud runs are run-scoped (each
run writes its own raw snapshot under runs/<run_id>/raw/ and the transform reads
only that snapshot) — so every run re-fetches all crawls and writes one raw
parquet batch per crawl (`...-statistics-<CRAWL>`). No watermark/state: an
incremental skip would make a later run's snapshot (and thus the published
table) contain only the newly-added crawls. The transform globs all batches via
the `common-crawl-statistics-*` layout.
"""
import json
import logging
from datetime import datetime

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)

logger = logging.getLogger(__name__)

COLLINFO_URL = "https://index.commoncrawl.org/collinfo.json"
STATS_URL = "https://data.commoncrawl.org/crawl-analysis/{crawl_id}/stats/part-00000.gz"

SCHEMA = pa.schema([
    ("crawl_id", pa.string()),
    ("crawl_date", pa.date32()),
    ("metric_family", pa.string()),
    ("key", pa.string()),
    ("count", pa.int64()),
])


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp.content


def _to_date(iso: str | None):
    """Parse a collinfo 'to' timestamp ('2026-05-21T22:06:58') to a date."""
    if not iso:
        return None
    try:
        return datetime.fromisoformat(iso.replace("Z", "+00:00")).date()
    except ValueError:
        logger.warning("common-crawl: unparseable crawl timestamp %r", iso)
        return None


def _dim(d) -> str:
    return d if isinstance(d, str) else json.dumps(d) if isinstance(d, (list, dict)) else str(d)


def _parse_stats(text: str, crawl_id: str, crawl_date) -> list[dict]:
    """Parse one crawl's stats file into long-format count rows.

    Each line is `<json-key>\t<value>`. The JSON key is an array
    `[metric_family, dim, crawl_id, *extra_dims]`; the value is a scalar page
    count, a `[pages, urls, ...]` list (we keep the leading page count), or a
    HyperLogLog sketch dict (size_estimate — not a count, dropped).

    Robustness: some older crawls emit a handful of malformed histogram keys
    missing the leading '[' (e.g. `"histogram", "url", ...]`); we repair those
    by prepending '['. Lines still unparseable after repair are counted and
    skipped, and we raise if more than a small fraction fails — a real format
    change should be loud, not silently dropped.
    """
    rows: list[dict] = []
    dropped = 0          # structurally-skipped (HLL sketches, non-count scalars)
    unparseable = 0      # lines we could not parse even after repair
    total = 0
    for line in text.splitlines():
        if not line.strip():
            continue
        total += 1
        key_part, sep, val_part = line.rpartition("\t")
        if not sep:
            unparseable += 1
            continue
        if not key_part.startswith("["):
            key_part = "[" + key_part  # repair the missing-bracket histogram lines
        try:
            arr = json.loads(key_part)
        except json.JSONDecodeError:
            unparseable += 1
            continue
        if not isinstance(arr, list) or len(arr) < 3:
            unparseable += 1
            continue
        family = arr[0]
        dims = [arr[1]] + arr[3:]  # element [2] is the crawl id; everything else is the key
        key = "/".join(_dim(d) for d in dims)
        try:
            count = int(val_part)
        except ValueError:
            try:
                v = json.loads(val_part)
            except json.JSONDecodeError:
                unparseable += 1
                continue
            if isinstance(v, list) and v and isinstance(v[0], int):
                count = v[0]
            else:
                dropped += 1  # HyperLogLog sketch or unexpected scalar
                continue
        rows.append({
            "crawl_id": crawl_id,
            "crawl_date": crawl_date,
            "metric_family": family,
            "key": key,
            "count": count,
        })

    if total and unparseable > max(100, total // 100):
        raise RuntimeError(
            f"common-crawl {crawl_id}: {unparseable}/{total} lines unparseable "
            "after repair — stats line format may have changed"
        )
    if dropped or unparseable:
        logger.info("common-crawl %s: dropped %d non-count, %d unparseable of %d",
                    crawl_id, dropped, unparseable, total)
    return rows


def fetch_statistics(node_id: str) -> None:
    """Re-fetch every crawl's stats file, writing one raw parquet batch per
    crawl into this run's raw snapshot. A crawl whose stats file is not yet
    published (404) is logged and skipped — it appears once the file lands."""
    import gzip

    crawls = _get_json(COLLINFO_URL)
    if not isinstance(crawls, list) or not crawls:
        raise RuntimeError(f"collinfo.json returned no crawls: {type(crawls)}")

    written = 0
    for c in crawls:
        crawl_id = c["id"]
        crawl_date = _to_date(c.get("to"))
        url = STATS_URL.format(crawl_id=crawl_id)
        try:
            raw = _get_bytes(url)
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 404:
                logger.warning("common-crawl %s: stats not published (404), skipping", crawl_id)
                continue
            raise

        text = gzip.decompress(raw).decode("utf-8")
        rows = _parse_stats(text, crawl_id, crawl_date)
        if not rows:
            raise RuntimeError(f"common-crawl {crawl_id}: parsed 0 count rows (format change?)")

        table = pa.Table.from_pylist(rows, schema=SCHEMA)
        save_raw_parquet(table, f"common-crawl-statistics-{crawl_id}")
        written += 1
        logger.info("common-crawl %s: wrote %d rows (%d/%d)",
                    crawl_id, len(table), written, len(crawls))

    if written == 0:
        raise RuntimeError("common-crawl: no crawl stats files fetched")


DOWNLOAD_SPECS = [
    NodeSpec(id="common-crawl-statistics", fn=fetch_statistics, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="common-crawl-statistics-transform",
        deps=["common-crawl-statistics"],
        sql='''
            SELECT
                crawl_id,
                CAST(crawl_date AS DATE)   AS crawl_date,
                metric_family,
                key,
                CAST("count" AS BIGINT)    AS count
            FROM "common-crawl-statistics"
            WHERE "count" IS NOT NULL
        ''',
    ),
]
