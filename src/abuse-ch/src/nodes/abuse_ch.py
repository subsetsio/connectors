"""abuse.ch connector — public bulk-export feeds across its threat-intel projects.

Mechanism: bulk_download (research-chosen). Each subset is one stable public
export URL returning the entire current dataset in a single GET (no auth, no
pagination, no incremental query) — so every fetch is a stateless full re-pull
that overwrites the prior snapshot. The query REST APIs are Auth-Key gated and
intentionally unused.

Feeds come in three containers: plain-text CSV (URLhaus URLs, SSLBL certs),
ZIP-wrapped CSV (URLhaus payloads, ThreatFox, MalwareBazaar), and a JSON array
(Feodo Tracker). Every CSV feed prepends a '#'-commented banner whose last
comment line is the (commented-out) column header, so we skip '#'-leading lines
and assign the known column names positionally. Raw is normalized to
newline-delimited JSON (ndjson) — CSV feeds stream row-by-row to ndjson.gz
(keeps the ~210MB MalwareBazaar dump off the heap), Feodo's small JSON array is
written via save_raw_ndjson. The SQL transforms cast/rename off the all-string
ndjson into the published Delta tables.
"""

from __future__ import annotations

import csv
import io
import json
import zipfile

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_writer,
    save_raw_ndjson,
    transient_retry,
)

_PREFIX = "abuse-ch-"

# entity_id -> feed descriptor. `columns` is the verbatim upstream column order
# (the commented-out header line of each feed); we assign these positionally
# because the real header is comment-prefixed. `skipinitialspace` handles the
# ", " field separator MalwareBazaar/ThreatFox use between quoted fields.
FEEDS: dict[str, dict] = {
    "urlhaus-urls": {
        "url": "https://urlhaus.abuse.ch/downloads/csv/",
        "container": "zip",
        "kind": "csv",
        "skipinitialspace": False,
        "columns": [
            "id", "dateadded", "url", "url_status", "last_online",
            "threat", "tags", "urlhaus_link", "reporter",
        ],
    },
    "urlhaus-payloads": {
        "url": "https://urlhaus.abuse.ch/downloads/payloads/",
        "container": "zip",
        "kind": "csv",
        "skipinitialspace": False,
        "columns": ["firstseen", "url", "filetype", "md5", "sha256", "signature"],
    },
    "malwarebazaar-samples": {
        "url": "https://bazaar.abuse.ch/export/csv/full/",
        "container": "zip",
        "kind": "csv",
        "skipinitialspace": True,
        "columns": [
            "first_seen_utc", "sha256_hash", "md5_hash", "sha1_hash", "reporter",
            "file_name", "file_type_guess", "mime_type", "signature", "clamav",
            "vtpercent", "imphash", "ssdeep", "tlsh",
        ],
    },
    "threatfox-iocs": {
        "url": "https://threatfox.abuse.ch/export/csv/full/",
        "container": "zip",
        "kind": "csv",
        "skipinitialspace": True,
        "columns": [
            "first_seen_utc", "ioc_id", "ioc_value", "ioc_type", "threat_type",
            "fk_malware", "malware_alias", "malware_printable", "last_seen_utc",
            "confidence_level", "is_compromised", "reference", "tags",
            "anonymous", "reporter",
        ],
    },
    "feodotracker-c2": {
        "url": "https://feodotracker.abuse.ch/downloads/ipblocklist.json",
        "container": "plain",
        "kind": "json",
    },
    "sslbl-certificates": {
        "url": "https://sslbl.abuse.ch/blacklist/sslblacklist.csv",
        "container": "plain",
        "kind": "csv",
        "skipinitialspace": False,
        "columns": ["listingdate", "sha1", "listingreason"],
    },
}


@transient_retry()
def _http_get(url: str) -> httpx.Response:
    # (connect, read) — generous read budget for the ~210MB MalwareBazaar dump.
    resp = get(url, timeout=(10.0, 300.0))
    resp.raise_for_status()
    return resp


def _emit_csv(text_stream, asset: str, columns: list[str], skipinitialspace: bool) -> None:
    """Stream the feed's data rows (skipping '#' banner lines) into ndjson.gz,
    one JSON object per row, keyed by the known column names. Bounded memory:
    nothing larger than one row is held at a time."""
    n = len(columns)
    reader = csv.reader(text_stream, skipinitialspace=skipinitialspace)
    written = 0
    with raw_writer(asset, "ndjson.gz", mode="wt", compression="gzip") as out:
        for row in reader:
            if not row or row[0].lstrip().startswith("#"):
                continue  # blank line or banner/comment
            if len(row) > n:
                # Unquoted trailing field (e.g. SSLBL reason) may contain commas:
                # fold the overflow back into the last column.
                row = row[: n - 1] + [",".join(row[n - 1:])]
            if len(row) < n:
                continue  # short/truncated line — not a real data row
            rec = {columns[i]: ((row[i].strip() or None)) for i in range(n)}
            out.write(json.dumps(rec, ensure_ascii=False))
            out.write("\n")
            written += 1
    if written == 0:
        raise AssertionError(f"{asset}: parsed 0 data rows from {asset} feed")


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    entity = node_id[len(_PREFIX):]
    cfg = FEEDS[entity]
    resp = _http_get(cfg["url"])

    if cfg["kind"] == "json":
        records = json.loads(resp.text)
        if not isinstance(records, list) or not records:
            raise AssertionError(f"{asset}: expected a non-empty JSON array, got {type(records).__name__}")
        save_raw_ndjson(records, asset)
        return

    if cfg["container"] == "zip":
        zf = zipfile.ZipFile(io.BytesIO(resp.content))
        member = zf.namelist()[0]
        with zf.open(member) as raw:
            stream = io.TextIOWrapper(raw, encoding="utf-8", errors="replace", newline="")
            _emit_csv(stream, asset, cfg["columns"], cfg["skipinitialspace"])
    else:
        stream = io.StringIO(resp.text, newline="")
        _emit_csv(stream, asset, cfg["columns"], cfg["skipinitialspace"])


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{_PREFIX}{eid}", fn=fetch_one, kind="download")
    for eid in FEEDS
]

# One published Delta table per feed — thin cast/rename off the all-string
# ndjson. TRY_CAST so a single malformed cell nulls rather than failing the run.
_SQL: dict[str, str] = {
    "urlhaus-urls": '''
        SELECT
            TRY_CAST(id AS BIGINT)              AS id,
            TRY_CAST(dateadded AS TIMESTAMP)    AS date_added,
            url,
            url_status,
            TRY_CAST(last_online AS TIMESTAMP)  AS last_online,
            threat,
            tags,
            urlhaus_link,
            reporter
        FROM "abuse-ch-urlhaus-urls"
        WHERE url IS NOT NULL
    ''',
    "urlhaus-payloads": '''
        SELECT
            TRY_CAST(firstseen AS TIMESTAMP)    AS first_seen,
            url,
            filetype,
            md5,
            sha256,
            signature
        FROM "abuse-ch-urlhaus-payloads"
        WHERE sha256 IS NOT NULL
    ''',
    "malwarebazaar-samples": '''
        SELECT
            TRY_CAST(first_seen_utc AS TIMESTAMP) AS first_seen_utc,
            sha256_hash,
            md5_hash,
            sha1_hash,
            reporter,
            file_name,
            file_type_guess,
            mime_type,
            signature,
            clamav,
            vtpercent,
            imphash,
            ssdeep,
            tlsh
        FROM "abuse-ch-malwarebazaar-samples"
        WHERE sha256_hash IS NOT NULL
    ''',
    "threatfox-iocs": '''
        SELECT
            TRY_CAST(first_seen_utc AS TIMESTAMP)    AS first_seen_utc,
            TRY_CAST(ioc_id AS BIGINT)               AS ioc_id,
            ioc_value,
            ioc_type,
            threat_type,
            fk_malware,
            malware_alias,
            malware_printable,
            TRY_CAST(last_seen_utc AS TIMESTAMP)     AS last_seen_utc,
            TRY_CAST(confidence_level AS INTEGER)    AS confidence_level,
            is_compromised,
            reference,
            tags,
            anonymous,
            reporter
        FROM "abuse-ch-threatfox-iocs"
        WHERE ioc_id IS NOT NULL
    ''',
    "feodotracker-c2": '''
        SELECT
            ip_address,
            TRY_CAST(port AS INTEGER)           AS port,
            status,
            hostname,
            TRY_CAST(as_number AS BIGINT)       AS as_number,
            as_name,
            country,
            TRY_CAST(first_seen AS TIMESTAMP)   AS first_seen,
            TRY_CAST(last_online AS DATE)       AS last_online,
            malware
        FROM "abuse-ch-feodotracker-c2"
        WHERE ip_address IS NOT NULL
    ''',
    "sslbl-certificates": '''
        SELECT
            TRY_CAST(listingdate AS TIMESTAMP)  AS listing_date,
            sha1,
            listingreason                        AS listing_reason
        FROM "abuse-ch-sslbl-certificates"
        WHERE sha1 IS NOT NULL
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_PREFIX}{eid}-transform",
        deps=[f"{_PREFIX}{eid}"],
        sql=_SQL[eid],
    )
    for eid in FEEDS
]
