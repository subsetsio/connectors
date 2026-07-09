"""BIS (Bank for International Settlements) connector.

Mechanism: bulk_csv. BIS publishes one persistent zipped flat CSV per
statistical topic (SDMX dataflow) at
``https://data.bis.org/static/bulk/<DATAFLOW_ID>_csv_flat.zip``. Each topic is a
single full-table snapshot — no pagination, no auth. We re-fetch the whole
corpus every run (stateless full re-pull): BIS revises history in place, so a
stored watermark would silently skip corrected observations. ``MAINTAIN_SPECS``
skips a topic whose ETag/Last-Modified is unchanged since the last success.

The flat SDMX CSV layout is uniform across dataflows: ``STRUCTURE``,
``STRUCTURE_ID``, ``ACTION``, then the dataflow's *dimension* columns, then
``TIME_PERIOD``, ``OBS_VALUE``, then attribute columns. The dimension set
differs per topic, so each topic's raw carries its own dimension columns
verbatim (code + label) rather than a shared opaque blob — the published table
for `WS_CBS_PUB` gets real `l_cp_country` / `l_rep_cty` columns, and the
profiler sees their cardinalities.

The largest topics (locational banking ~37M rows, debt securities ~19M) stream
row-group-batched into Parquet so memory stays bounded.
"""
import csv
import datetime
import io
import math
import os
import re
import tempfile
import time
import zipfile

import httpx
import pyarrow as pa

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    get_client,
    is_transient,
    raw_asset_exists,
    raw_parquet_writer,
    record_source_signature,
    source_unchanged,
)

# The accepted entity union — one BIS dataflow per id. WS_NA_SEC_C3 is
# intentionally absent: the dataflow is registered structurally but publishes no
# observations (bulk file 404s, SDMX /data returns "No data for data query"), so
# the accept stage deferred it.
from constants import ENTITY_IDS

BULK_URL = "https://data.bis.org/static/bulk/{flow}_csv_flat.zip"

# Row-group batch size for streaming the (multi-GB uncompressed) flat CSV into
# Parquet without building the whole table in memory.
BATCH_ROWS = 100_000

# (connect, read) seconds. Read is generous: the largest topic is ~350 MB.
_TIMEOUT = (15.0, 600.0)
_DOWNLOAD_ATTEMPTS = 8
_CHUNK = 1 << 20  # 1 MiB

# Columns the SDMX flat layout always carries around the dimension block. Used
# to locate the dimension slice; never emitted as dimensions themselves.
_STRUCTURAL = ("STRUCTURE", "STRUCTURE_ID", "ACTION")

# SDMX period formats observed across all 27 BIS topics (freq codes A/Q/M/D/H).
_PERIOD_PATTERNS = (
    (re.compile(r"^(\d{4})-(\d{2})-(\d{2})$"), lambda m: (int(m[1]), int(m[2]), int(m[3]))),
    (re.compile(r"^(\d{4})-(\d{2})$"), lambda m: (int(m[1]), int(m[2]), 1)),
    (re.compile(r"^(\d{4})-Q([1-4])$"), lambda m: (int(m[1]), (int(m[2]) - 1) * 3 + 1, 1)),
    (re.compile(r"^(\d{4})-S([12])$"), lambda m: (int(m[1]), (int(m[2]) - 1) * 6 + 1, 1)),
    (re.compile(r"^(\d{4})$"), lambda m: (int(m[1]), 1, 1)),
)


def _download_zip_to(url: str, dest_path: str) -> None:
    """Stream a bulk zip to ``dest_path``, resuming via HTTP Range on drops.

    BIS serves the largest topics (locational/consolidated banking ~350 MB) from
    a static host that occasionally closes the connection mid-body — a buffered
    ``.content`` read of the whole file then fails with RemoteProtocolError and a
    plain retry re-downloads from byte 0 (and tends to drop at the same offset).
    Instead we stream to disk and, on a transient drop, re-request only the
    missing tail with ``Range: bytes=<have>-``. We send ``Accept-Encoding:
    identity`` and use ``iter_raw`` so on-the-wire byte offsets match the file
    (a zip is already compressed, so the server returns it uncompressed anyway).
    """
    client = get_client()
    have = 0
    expected = None
    last_exc = None

    for attempt in range(_DOWNLOAD_ATTEMPTS):
        headers = {"Accept-Encoding": "identity"}
        if have:
            headers["Range"] = f"bytes={have}-"
        try:
            with client.stream("GET", url, headers=headers, timeout=_TIMEOUT) as resp:
                # Server ignored our Range (full 200 instead of 206 partial):
                # restart from scratch so we don't append a second full copy.
                if have and resp.status_code == 200:
                    have = 0
                # 416 = we already have the whole file; nothing left to fetch.
                if have and resp.status_code == 416:
                    return
                resp.raise_for_status()

                if expected is None:
                    cl = resp.headers.get("Content-Length")
                    # On a 206 the length is of the *remaining* range, so only
                    # trust Content-Length to set the total on a fresh 200.
                    if cl is not None and resp.status_code == 200:
                        expected = int(cl)

                mode = "ab" if have else "wb"
                with open(dest_path, mode) as fh:
                    for chunk in resp.iter_raw(_CHUNK):
                        fh.write(chunk)
                        have += len(chunk)

            # Stream ended cleanly. Guard against a silent short read.
            if expected is not None and have < expected:
                raise httpx.RemoteProtocolError(
                    f"short read: have {have} of {expected} bytes"
                )
            return
        except Exception as exc:  # noqa: BLE001 - re-raise non-transient below
            if not is_transient(exc):
                raise
            last_exc = exc
            # Exponential backoff, capped; keep `have` so we resume the tail.
            time.sleep(min(4 * 2 ** attempt, 120))

    raise last_exc


def _flow_from_node(node_id: str) -> str:
    # node id is f"bis-{flow.lower().replace('_', '-')}" -> recover the flow id.
    return node_id[len("bis-"):].upper().replace("-", "_")


def _split_coded(value: str) -> tuple[str, str | None]:
    """SDMX coded cells look like ``"KW: Kuwait"`` -> ``("KW", "Kuwait")``."""
    if not value:
        return "", None
    code, sep, label = value.partition(": ")
    if not sep:
        return value.strip(), None
    return code.strip(), label.strip() or None


def _to_float(value: str):
    value = value.strip()
    if value == "":
        return None
    try:
        f = float(value)
    except ValueError:
        return None
    # BIS encodes missing/holiday/not-collected observations as the literal
    # string "NaN" (see OBS_STATUS M/L/H). float() happily parses those to a NaN
    # double, which is NOT NULL and would otherwise leak past the transform's
    # IS NOT NULL gate as a junk "observation". Treat any non-finite value as
    # missing so raw carries a clean None.
    if not math.isfinite(f):
        return None
    return f


def _period_start(period: str, flow: str):
    """Map an SDMX TIME_PERIOD to the first calendar day of the period.

    Raises on an unrecognised format: a new frequency is source drift we must
    map deliberately, not silently null out. Every period in all 27 topics
    matches one of `_PERIOD_PATTERNS`.
    """
    for pattern, to_ymd in _PERIOD_PATTERNS:
        m = pattern.match(period)
        if m:
            return datetime.date(*to_ymd(m))
    raise ValueError(f"{flow}: unrecognised TIME_PERIOD format {period!r}")


def _repair_header(header: list[str]) -> list[str]:
    """Re-join header cells the CSV reader split on a comma inside a label.

    BIS does not quote the header's ``CODE:Description`` labels, so a label
    containing a comma (``STO:Stocks, Transactions, Other Flows``,
    ``EXPENDITURE:Expenditure (COFOG, COICOP, COPP or COPNI)``) is split into
    spurious extra cells, shifting every column after it — TIME_PERIOD and
    OBS_VALUE then resolve to the wrong index and read empty. The real
    inter-column separator is a bare comma while a comma inside a label is
    always followed by a space, so any fragment beginning with whitespace
    continues the previous cell. Data rows are properly quoted; only the header
    needs repair.
    """
    merged: list[str] = []
    for cell in header:
        if merged and cell[:1].isspace():
            merged[-1] = merged[-1] + "," + cell
        else:
            merged.append(cell)
    return merged


def _build_schema(codes: list[str], dim_idx: list[int], attr_idx: list[int]) -> pa.Schema:
    """The topic's raw schema: identity, its own dimensions, observation, attributes."""
    fields = [
        ("dataflow", pa.string()),
        ("series_key", pa.string()),
    ]
    for i in dim_idx:
        name = codes[i].lower()
        fields.append((name, pa.string()))
        fields.append((f"{name}_label", pa.string()))
    fields += [
        ("time_period", pa.string()),
        ("period_start", pa.date32()),
        ("obs_value", pa.float64()),
    ]
    fields += [(codes[i].lower(), pa.string()) for i in attr_idx]
    return pa.schema(fields)


def fetch_one(node_id: str) -> None:
    """Download one BIS topic's flat-CSV bulk zip and write normalised Parquet.

    Stateless full snapshot: the whole topic is re-fetched and overwritten every
    run. Freshness gating is the maintain step's job.
    """
    asset = node_id
    flow = _flow_from_node(node_id)
    url = BULK_URL.format(flow=flow)

    fd, tmp_path = tempfile.mkstemp(prefix=f"{asset}-", suffix=".zip")
    os.close(fd)
    try:
        _download_zip_to(url, tmp_path)
        with zipfile.ZipFile(tmp_path) as zf:
            _ingest_member(zf, zf.namelist()[0], asset, flow)
    finally:
        os.remove(tmp_path)

    record_source_signature(asset, url)


def _ingest_member(zf: zipfile.ZipFile, member: str, asset: str, flow: str) -> None:
    """Stream one flat-CSV member of a BIS bulk zip into normalised Parquet."""
    with zf.open(member) as fh:
        text = io.TextIOWrapper(fh, encoding="utf-8-sig", newline="")
        reader = csv.reader(text)
        header = _repair_header(next(reader))
        codes = [h.split(":", 1)[0].strip() for h in header]

        if len(set(codes)) != len(codes):
            raise ValueError(f"{flow}: duplicate column codes in header {codes}")

        # SDMX flat layout: STRUCTURE, STRUCTURE_ID, ACTION, <dimensions...>,
        # TIME_PERIOD, OBS_VALUE, <attributes...>.
        ti = codes.index("TIME_PERIOD")
        vi = codes.index("OBS_VALUE")
        if codes[:3] != list(_STRUCTURAL) or vi != ti + 1:
            raise ValueError(f"{flow}: unexpected SDMX flat layout {codes}")

        dim_idx = list(range(len(_STRUCTURAL), ti))
        attr_idx = list(range(vi + 1, len(codes)))
        schema = _build_schema(codes, dim_idx, attr_idx)
        ncols = len(header)

        empty = lambda: {name: [] for name in schema.names}
        batch = empty()
        pending = 0

        with raw_parquet_writer(asset, schema) as writer:
            for row in reader:
                if len(row) < ncols:
                    row = row + [""] * (ncols - len(row))

                # The bulk file interleaves series-metadata rows (no TIME_PERIOD,
                # no OBS_VALUE, attribute-only) with observation rows. They aren't
                # observations — keeping them pollutes the raw with empty-period
                # rows that collide on (series_key, time_period).
                period = row[ti].strip()
                if not period:
                    continue

                key_parts = []
                for i in dim_idx:
                    name = codes[i].lower()
                    code, label = _split_coded(row[i])
                    batch[name].append(code)
                    batch[f"{name}_label"].append(label)
                    key_parts.append(code)

                batch["dataflow"].append(flow)
                batch["series_key"].append(".".join(key_parts))
                batch["time_period"].append(period)
                batch["period_start"].append(_period_start(period, flow))
                batch["obs_value"].append(_to_float(row[vi]))
                for i in attr_idx:
                    batch[codes[i].lower()].append(row[i] or None)
                pending += 1

                if pending >= BATCH_ROWS:
                    writer.write_table(pa.table(batch, schema=schema))
                    batch = empty()
                    pending = 0

            if pending:
                writer.write_table(pa.table(batch, schema=schema))


def _is_fresh(asset_id: str) -> bool:
    flow = _flow_from_node(asset_id)
    return source_unchanged(asset_id, BULK_URL.format(flow=flow)) and raw_asset_exists(
        asset_id, "parquet"
    )


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bis-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# BIS publishes each topic on its own schedule (daily policy rates through
# annual CPMI surveys) per https://www.bis.org/statistics/relcal.htm. Rather
# than encode 27 cadences, we let the bulk file's own ETag/Last-Modified decide:
# every zip under /static/bulk/ serves both validators.
MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=spec.id,
        description=(
            "Re-fetched whenever the topic's bulk zip changes (ETag/Last-Modified "
            "on https://data.bis.org/static/bulk/); per-topic release schedule at "
            "https://www.bis.org/statistics/relcal.htm"
        ),
        check=_is_fresh,
    )
    for spec in DOWNLOAD_SPECS
]
