"""RIPE NCC — rir-allocations.

The RIPE NCC delegated-stats registry: one row per allocated/assigned
number-resource block (ipv4 / ipv6 / asn), with country, size, allocation date
and status. Pipe-delimited RIR statistics exchange format, ~260k records,
~18MB, daily snapshot at a stable URL. No auth.
"""

import io

import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_parquet,
    transient_retry,
)


@transient_retry()
def _get_bytes(url: str) -> bytes:
    resp = get(url, timeout=(30.0, 300.0))
    resp.raise_for_status()
    return resp.content


RIR_URL = "https://ftp.ripe.net/pub/stats/ripencc/delegated-ripencc-extended-latest"

RIR_FIELDS = (
    "registry",
    "country",
    "type",
    "start",
    "value",
    "date",
    "status",
    "opaque_id",
)

RIR_SCHEMA = pa.schema([(f, pa.string()) for f in RIR_FIELDS])


def fetch_rir_allocations(node_id: str) -> None:
    asset = node_id
    text = _get_bytes(RIR_URL).decode("utf-8", "replace")
    rows = []
    for line in io.StringIO(text):
        line = line.rstrip("\n")
        if not line or line.startswith("2|"):
            continue  # header/version line
        parts = line.split("|")
        if len(parts) < 7 or parts[-1] == "summary":
            continue  # summary lines and malformed rows
        # registry|cc|type|start|value|date|status|opaque_id[|extensions]
        rows.append({f: (parts[i] if i < len(parts) else None)
                     for i, f in enumerate(RIR_FIELDS)})
    table = pa.Table.from_pylist(rows, schema=RIR_SCHEMA)
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="ripe-ncc-rir-allocations",
        fn=fetch_rir_allocations,
        kind="download",
    ),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ripe-ncc-rir-allocations-transform",
        deps=["ripe-ncc-rir-allocations"],
        sql='''
            SELECT
                registry,
                NULLIF(country, '')                       AS country,
                type,
                start,
                TRY_CAST(value AS BIGINT)                 AS value,
                TRY_STRPTIME(NULLIF(date, ''), '%Y%m%d')::DATE AS allocation_date,
                status,
                opaque_id
            FROM "ripe-ncc-rir-allocations"
            WHERE type IN ('ipv4', 'ipv6', 'asn')
        ''',
    ),
]
