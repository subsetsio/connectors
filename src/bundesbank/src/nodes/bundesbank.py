"""Bundesbank SDMX 2.1 statistics — one raw asset per dataflow.

Fetch shape: stateless full re-pull. Each accepted dataflow is a single bulk
request; the API exposes no change feed, so re-fetching in full every run picks up
Bundesbank's frequent back-revisions for free, with no watermark to go stale.

## Wire format — why csv-zip

`GET /rest/data/{flowRef}` with `Accept: application/vnd.bbk.data+csv-zip` returns
a ZIP of Bundesbank's own wide SDMX-CSV. Two other surfaces exist and neither can
serve this corpus:

- `?format=csv` (single wide CSV) rejects dataflows with mixed frequencies (400),
  with real-time vintages (406), and with more than 200 series (406) -- each time
  naming this csv-zip media type as the remedy.
- `Accept: application/vnd.sdmx.data+csv` (standard long SDMX-CSV) repeats the
  title, unit and every dimension on each observation, which explodes the payload
  ~100-160x: BBSSY is 1.5MB as csv-zip and 202MB long; BBBK1 is 13.8MB against
  2.24GB. Past a few hundred MB the server switches to asynchronous preparation
  and answers 413 "being prepared, retry later" (BBBK7: 3 min, BBKRT: 20 min).

csv-zip returned 200 promptly for every dataflow probed, including the three that
defeat the other two surfaces, so it is the single code path here. 413 is still
classified as retryable below: it is the server's "preparing, come back" signal,
not a size cap, and a dataflow that grows could start tripping it.

## Wide-matrix layout

Each CSV inside the ZIP holds one (dataflow, frequency, <=200-series chunk).
It is semicolon-delimited, with a header block of *variable* length:

    row 0    ""                     <series key>   <series key>_FLAGS  ...
    row 1    ""                     <German label>  ""                 ...
    rows 2+  <German attribute>     <per-series attribute value>       ...
    rows N+  <time period>          <value>        <flag>              ...

The attribute rows differ per dataflow -- BBDA1 carries `Quelle` and
`Umrechnungsart`, BBKRT carries `Basisjahr` and `Originalkennung` -- so the block
is delimited by content, not by a fixed row count: data begins at the first row
whose first cell parses as a time period. Attributes that recur across the corpus
are promoted to columns; the rest are preserved verbatim as JSON in `attributes`,
so nothing the source published is dropped.

## Two column shapes

In most dataflows a column is a time series and its row-0 header is the SDMX
series key. In BBKRT (real-time data) a column is instead a release *vintage* and
the header is that vintage's date (`28.04.2005`); the series identity lives in the
filename, and there are no `_FLAGS` columns at all. `file_key` therefore carries
the filename stem in both shapes and `series_key` the row-0 header, so a transform
can address either without a per-dataflow branch here.

## Values

German-formatted: `,` is the decimal separator and no thousands separator is used.
Three sentinels share the value column and two of them mean opposite things --
`.` (unknown/suppressed) and `...` ("Angaben fallen später an", not published
yet) are missing observations, while `-` is "Nichts vorhanden", exactly zero
(all three readings are confirmed by the paired `_FLAGS` text; see
MISSING_VALUES).

Missing observations are dropped rather than materialised as nulls: these are
sparse matrices whose series start decades apart, and a null row per absent cell
would multiply the corpus severalfold to say nothing. Zeros are kept, because a
zero balance is an observation.

## Freshness

No `MAINTAIN_SPECS`. The data endpoint returns neither `ETag` nor `Last-Modified`
(only `cache-control: max-age`), so `source_unchanged` could never return True,
and the per-dataflow release cadence runs from daily (BBSSY) to annual, which no
single age window fits. Production refresh cadence lives in `maintenance.json`.
"""

import csv
import io
import json
import re
import zipfile
from datetime import date
from itertools import chain

import httpx
import pyarrow as pa
from constants import ENTITY_IDS
from subsets_utils import NodeSpec, get, is_transient, raw_parquet_writer
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

BASE_URL = "https://api.statistiken.bundesbank.de/rest/data"
CSV_ZIP_MEDIA_TYPE = "application/vnd.bbk.data+csv-zip;version=1.0.0"

# Time periods as this CSV renders them: 2026, 2026-05, 2026-07-08, 2026-Q1,
# 2026-S2 (half-years; the file is named .H but the period reads S), 2026-W03.
PERIOD_RE = re.compile(r"^\d{4}(?:-(?:\d{2}(?:-\d{2})?|Q[1-4]|[SH][12]|W\d{2}))?$")

# `BBSAP.M(02).csv` -- the `(02)` is the >200-series chunk counter, not identity.
CHUNK_SUFFIX_RE = re.compile(r"\(\d+\)$")

FLAG_SUFFIX = "_FLAGS"

# The German statistical legend, confirmed against the paired `_FLAGS` column:
#   "."  -> flagged `Kein Wert vorhanden` / `Fehlender Wert (unterdrückt)`
#           = unknown or suppressed. Genuinely missing.
#   "..." -> flagged `Angaben fallen später an` = "figures follow later": the
#           period exists but has not been published yet. Missing, not zero.
#   ""   -> unflagged padding of a ragged matrix (BBKRT's vintage columns).
#           Also missing.
#   "-"  -> flagged `Nichts vorhanden` = "nothing present", i.e. EXACTLY ZERO.
#           Never once flagged as a missing value anywhere in the corpus.
# Conflating the last with the others would silently delete ~1.65M real zeros
# from the banking statistics, where a zero balance is an observation.
MISSING_VALUES = {"", ".", "..."}
ZERO_VALUE = "-"

# Attribute rows recurring across dataflows, promoted from `attributes` to
# first-class columns. Every attribute row is kept in `attributes` regardless.
PROMOTED_ATTRS = {
    "unit": "Einheit",
    "unit_en": "BBK_UNIT_ENG",
    "magnitude": "Dimension",  # Eins / Millionen / Milliarden
    "category": "Kategorie",
    "last_update": "Stand vom",
}
DECIMALS_ATTR = "Dezimalstellen"

QUARTER_START_MONTH = {"Q1": 1, "Q2": 4, "Q3": 7, "Q4": 10}
HALF_START_MONTH = {"S1": 1, "S2": 7, "H1": 1, "H2": 7}

# Bound the row buffer: one CSV can expand to millions of long-format rows
# (BBSSY carries 200 daily series over 30 years), and spawn-context RSS is the
# hard ceiling for a spec.
BATCH_ROWS = 250_000

# Every string column here is constant across a whole series (or a whole file),
# so a long-format row repeats it once per observation. Dictionary-encoding them
# keeps that free: identical on disk, but ~9x smaller once a reader materialises
# the table -- and BBKRT's 21.6M rows carry a ~200-byte `attributes` JSON that
# would otherwise decode to several GB. DuckDB reads the encoding transparently.
DICT = pa.dictionary(pa.int32(), pa.string())

SCHEMA = pa.schema(
    [
        pa.field("dataflow", DICT, nullable=False),
        pa.field("file_key", DICT, nullable=False),
        pa.field("frequency", DICT, nullable=False),
        pa.field("series_key", DICT, nullable=False),
        pa.field("label", DICT),
        pa.field("time_period", DICT, nullable=False),
        pa.field("period_start", pa.date32(), nullable=False),
        pa.field("value", pa.float64(), nullable=False),
        pa.field("flag", DICT),
        pa.field("unit", DICT),
        pa.field("unit_en", DICT),
        pa.field("magnitude", DICT),
        pa.field("decimals", pa.int32()),
        pa.field("category", DICT),
        pa.field("last_update", DICT),
        pa.field("attributes", DICT),
    ]
)


def _preparing_or_transient(exc: BaseException) -> bool:
    """The standard transient set, plus HTTP 413.

    On this API 413 does not mean "too large" -- it means "this dataset is being
    assembled server-side, retry later" (the body carries an ETA). The identical
    request returns 200 once preparation completes, and the result is cached.
    """
    if isinstance(exc, httpx.HTTPStatusError) and exc.response.status_code == 413:
        return True
    return is_transient(exc)


@retry(
    retry=retry_if_exception(_preparing_or_transient),
    stop=stop_after_attempt(10),
    wait=wait_exponential(min=8, max=120),
    reraise=True,
)
def _fetch_zip(dataflow: str) -> bytes:
    resp = get(
        f"{BASE_URL}/{dataflow}",
        headers={"Accept": CSV_ZIP_MEDIA_TYPE},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    return resp.content


def _period_start(period: str) -> date:
    """First calendar day of an SDMX time period."""
    year = int(period[:4])
    if len(period) == 4:
        return date(year, 1, 1)
    rest = period[5:]
    if len(rest) == 2 and rest.isdigit():
        return date(year, int(rest), 1)
    if len(rest) == 5 and rest[2] == "-":
        return date(year, int(rest[:2]), int(rest[3:]))
    if rest in QUARTER_START_MONTH:
        return date(year, QUARTER_START_MONTH[rest], 1)
    if rest in HALF_START_MONTH:
        return date(year, HALF_START_MONTH[rest], 1)
    if rest.startswith("W"):
        return date.fromisocalendar(year, int(rest[1:]), 1)
    raise ValueError(f"unrecognised time period: {period!r}")


def _parse_value(raw: str) -> float | None:
    token = raw.strip()
    if token in MISSING_VALUES:
        return None
    if token == ZERO_VALUE:
        return 0.0
    # German formatting: `,` is the decimal separator. No thousands separator is
    # emitted today, but strip `.` when both appear so a future change cannot
    # silently read 1.234,5 as 1.234.
    if "," in token:
        token = token.replace(".", "").replace(",", ".")
    return float(token)


def _cell(row: list[str], idx: int) -> str:
    return row[idx].strip() if idx < len(row) else ""


def _column_layout(
    header: list[str], dataflow: str, filename: str
) -> list[tuple[int, str, int | None]]:
    """Pair each value column with its optional `_FLAGS` column.

    Returns (value_idx, series_key, flag_idx | None). BBKRT emits no flag columns
    at all, so the pairing is positional and optional rather than assumed.
    """
    layout: list[tuple[int, str, int | None]] = []
    idx = 1  # column 0 is the period / attribute-name gutter
    while idx < len(header):
        key = header[idx].strip()
        if not key:
            idx += 1
            continue
        if key.endswith(FLAG_SUFFIX):
            raise ValueError(
                f"{dataflow}/{filename}: flags column {key!r} has no preceding value column"
            )
        flag_idx = None
        if idx + 1 < len(header) and header[idx + 1].strip() == key + FLAG_SUFFIX:
            flag_idx = idx + 1
        layout.append((idx, key, flag_idx))
        idx += 2 if flag_idx is not None else 1
    if not layout:
        raise ValueError(f"{dataflow}/{filename}: header row declares no series columns")
    return layout


def _new_buffer() -> dict[str, list]:
    return {field.name: [] for field in SCHEMA}


def _flush(writer, buffer: dict[str, list]) -> int:
    rows = len(buffer["series_key"])
    if rows:
        writer.write_table(pa.Table.from_pydict(buffer, schema=SCHEMA))
        for column in buffer.values():
            column.clear()
    return rows


def _describe_columns(
    header: list[str], labels: list[str], attribute_rows: dict[str, list[str]],
    dataflow: str, filename: str,
) -> list[dict]:
    """Per-column constants, resolved once rather than per observation."""
    columns = []
    for value_idx, series_key, flag_idx in _column_layout(header, dataflow, filename):
        attributes = {
            name: _cell(row, value_idx)
            for name, row in attribute_rows.items()
            if _cell(row, value_idx)
        }
        decimals = attributes.get(DECIMALS_ATTR, "")
        columns.append(
            {
                "value_idx": value_idx,
                "flag_idx": flag_idx,
                "series_key": series_key,
                "label": _cell(labels, value_idx) or None,
                "decimals": int(decimals) if decimals.isdigit() else None,
                "promoted": {
                    column: attributes.get(attr) for column, attr in PROMOTED_ATTRS.items()
                },
                "attributes": json.dumps(attributes, ensure_ascii=False, sort_keys=True),
            }
        )
    return columns


def _parse_member(dataflow: str, filename: str, handle, writer, buffer: dict[str, list]) -> int:
    """Stream one member CSV into `writer` as long-format rows. Returns rows written."""
    reader = csv.reader(io.TextIOWrapper(handle, encoding="utf-8-sig", newline=""), delimiter=";")

    # The header block runs until the first row whose gutter cell is a time
    # period. Its length varies per dataflow, so it cannot be skipped by count.
    header_rows: list[list[str]] = []
    first_data_row = None
    for row in reader:
        if row and PERIOD_RE.match(row[0].strip()):
            first_data_row = row
            break
        header_rows.append(row)

    if first_data_row is None:
        raise ValueError(
            f"{dataflow}/{filename}: no row begins with a time period - "
            "the header block or the period format changed"
        )
    if len(header_rows) < 2:
        raise ValueError(f"{dataflow}/{filename}: header block is missing its key or label row")

    file_key = CHUNK_SUFFIX_RE.sub("", filename.rsplit("/", 1)[-1].removesuffix(".csv"))
    key_parts = file_key.split(".")
    if len(key_parts) < 2 or not key_parts[1]:
        raise ValueError(f"{dataflow}/{filename}: cannot read a frequency from {file_key!r}")
    frequency = key_parts[1]

    columns = _describe_columns(
        header_rows[0],
        header_rows[1],
        {row[0].strip(): row for row in header_rows[2:] if row and row[0].strip()},
        dataflow,
        filename,
    )

    written = 0
    # The first data row was consumed while locating the end of the header block.
    for row in chain([first_data_row], reader):
        if not row or not row[0].strip():
            continue  # trailing blank line
        period = row[0].strip()
        if not PERIOD_RE.match(period):
            raise ValueError(
                f"{dataflow}/{filename}: unexpected row {period!r} below the data block"
            )
        period_start = _period_start(period)
        for column in columns:
            value = _parse_value(_cell(row, column["value_idx"]))
            if value is None:
                continue  # sparse matrix: an absent observation, not a null one
            flag = _cell(row, column["flag_idx"]) if column["flag_idx"] is not None else ""
            buffer["dataflow"].append(dataflow)
            buffer["file_key"].append(file_key)
            buffer["frequency"].append(frequency)
            buffer["series_key"].append(column["series_key"])
            buffer["label"].append(column["label"])
            buffer["time_period"].append(period)
            buffer["period_start"].append(period_start)
            buffer["value"].append(value)
            buffer["flag"].append(flag or None)
            for name, attr_value in column["promoted"].items():
                buffer[name].append(attr_value)
            buffer["decimals"].append(column["decimals"])
            buffer["attributes"].append(column["attributes"])
        if len(buffer["series_key"]) >= BATCH_ROWS:
            written += _flush(writer, buffer)

    return written


def fetch_one(node_id: str) -> None:
    asset = node_id  # the runtime hands us the spec id; it IS the asset name
    dataflow = node_id.removeprefix("bundesbank-").upper()

    payload = _fetch_zip(dataflow)
    if not payload:
        # Observed live: this API answers 200 with a zero-byte body for some query
        # shapes. Treat that as a failure, never as an empty dataflow.
        raise RuntimeError(f"{dataflow}: API returned an empty body for {BASE_URL}/{dataflow}")

    archive = zipfile.ZipFile(io.BytesIO(payload))
    members = sorted(n for n in archive.namelist() if n.lower().endswith(".csv"))
    if not members:
        raise RuntimeError(f"{dataflow}: csv-zip archive holds no CSV members")

    written = 0
    with raw_parquet_writer(asset, SCHEMA) as writer:
        buffer = _new_buffer()
        for member in members:
            with archive.open(member) as handle:
                written += _parse_member(dataflow, member, handle, writer, buffer)
        written += _flush(writer, buffer)

    if not written:
        raise RuntimeError(
            f"{dataflow}: parsed {len(members)} CSV member(s) but produced no observations"
        )
    print(f"  {dataflow}: {written} observations from {len(members)} CSV member(s)")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"bundesbank-{entity_id.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]
