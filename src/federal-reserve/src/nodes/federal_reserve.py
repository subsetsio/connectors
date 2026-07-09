"""Federal Reserve Board — Data Download Program (DDP) connector.

Each of the 16 rank-accepted statistical releases (H.15, Z.1, G.17, ...) is
downloaded as a single full-release SDMX-ML 1.0 zip from the DDP:

    https://www.federalreserve.gov/datadownload/Output.aspx?rel=<REL>&filetype=zip

The zip carries <REL>_data.xml (all series, all observations), a structure
file and XSDs. We stream-parse the data XML (Z.1 alone is ~590MB uncompressed)
and emit one raw parquet row per observation. Every release is a stateless full
re-pull each refresh — the SDMX dump is a complete snapshot, so revisions and
late corrections are picked up for free and the raw is simply overwritten. No
watermark / cursor: the DDP exposes no incremental-delta filter we rely on, and
a full re-pull of one release is a single request of at most tens of MB zipped.

Series-level key dimensions differ per release (H.15 has INSTRUMENT/MATURITY,
DSR has DEBT/TYPE, ...), so the raw schema keeps a fixed core of columns and
stuffs the full per-series attribute set into a JSON `series_attributes` column.
Each release publishes its own Delta table (its own series namespace), so the
transforms share one uniform SQL template.

A release's data XML groups its <Series> under one <DataSet> per presentation
table (G.17 has 14: IP_MARKET_GROUPS, IP_SPECIAL_AGGREGATES, CAPUTL, ...). A
headline series is repeated verbatim under every table it appears in, so
`series_name` alone does not identify a raw row — `dataset_id` does, together
with the series and period. The repeats carry identical observations; the
transforms collapse them.
"""

import io
import json
import zipfile
import xml.etree.ElementTree as ET

import pyarrow as pa
import pyarrow.parquet as pq

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    configure_http,
    raw_parquet_writer,
    transient_retry,
)

# The entity union — one DDP release code per rank-accepted subset.
from constants import ENTITY_IDS

_BASE_URL = "https://www.federalreserve.gov/datadownload/Output.aspx"

# Browser-like UA: the DDP is fronted by Cloudflare, which serves an HTML
# challenge to some non-browser agents instead of the zip. ASCII-only.
_USER_AGENT = "Mozilla/5.0 (compatible; subsets-connector/1.0; +https://subsets.io)"

# Standard FRB SDMX frequency codes (frb_common codelist CL_FREQ — shared across
# every release). Fallback to the raw code for anything unmapped.
_FREQ = {
    "0": "Undefined", "8": "Daily", "9": "Business day",
    "16": "Weekly (Sunday)", "17": "Weekly (Monday)", "18": "Weekly (Tuesday)",
    "19": "Weekly (Wednesday)", "20": "Weekly (Thursday)", "21": "Weekly (Friday)",
    "22": "Weekly (Saturday)", "32": "Tenday",
    "64": "Bi-Weekly (ASunday)", "65": "Bi-Weekly (AMonday)", "66": "Bi-Weekly (ATuesday)",
    "67": "Bi-Weekly (AWednesday)", "68": "Bi-Weekly (AThursday)", "69": "Bi-Weekly (AFriday)",
    "70": "Bi-Weekly (ASaturday)", "71": "Bi-Weekly (BSunday)", "72": "Bi-Weekly (BMonday)",
    "73": "Bi-Weekly (BTuesday)", "74": "Bi-Weekly (BWednesday)", "75": "Bi-Weekly (BThursday)",
    "76": "Bi-Weekly (BFriday)", "77": "Bi-Weekly (BSaturday)",
    "128": "Twice Monthly", "129": "Monthly",
    "144": "Bi-Monthly (Nov)", "145": "Bi-Monthly",
    "160": "Quarterly (Oct)", "161": "Quarterly (Nov)", "162": "Quarterly",
    "192": "Annual (Jan)", "193": "Annual (Feb)", "194": "Annual (Mar)",
    "195": "Annual (Apr)", "196": "Annual (May)", "197": "Annual (Jun)",
    "198": "Annual (Jul)", "199": "Annual (Aug)", "200": "Annual (Sep)",
    "201": "Annual (Oct)", "202": "Annual (Nov)", "203": "Annual",
    "204": "Semi-Annual (Jul)", "205": "Semi-Annual (Aug)", "206": "Semi-Annual (Sep)",
    "207": "Semi-Annual (Oct)", "208": "Semi-Annual (Nov)", "209": "Semi-Annual",
}

# Fixed raw schema: a uniform core + the full per-series attribute set as JSON.
SCHEMA = pa.schema([
    ("release", pa.string()),
    ("dataset_id", pa.string()),
    ("series_name", pa.string()),
    ("freq_code", pa.string()),
    ("frequency", pa.string()),
    ("unit", pa.string()),
    ("unit_mult", pa.string()),
    ("currency", pa.string()),
    ("short_description", pa.string()),
    ("long_description", pa.string()),
    ("series_attributes", pa.string()),
    ("time_period", pa.string()),
    ("obs_value", pa.float64()),
    ("obs_status", pa.string()),
])

_BATCH_ROWS = 250_000  # flush a parquet row group roughly every quarter-million obs


@transient_retry()
def _fetch_zip(rel: str) -> bytes:
    """Fetch the full-release SDMX zip for one release code."""
    resp = get(
        _BASE_URL,
        params={"rel": rel, "filetype": "zip"},
        timeout=(10.0, 300.0),
    )
    resp.raise_for_status()
    ctype = resp.headers.get("content-type", "")
    body = resp.content
    # Cloudflare challenge / error pages come back as HTML with a 200 — detect
    # the format mismatch loudly instead of trying to parse HTML as a zip.
    if "zip" not in ctype.lower() and not body[:2] == b"PK":
        raise RuntimeError(
            f"rel={rel}: expected a zip, got content-type={ctype!r} "
            f"({len(body)} bytes, starts {body[:16]!r})"
        )
    return body


def _localname(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def _parse_obs_value(raw):
    if raw is None or raw == "":
        return None
    try:
        return float(raw)
    except (TypeError, ValueError):
        return None


def _series_rows(series_el, release: str, dataset_id: str):
    """Yield one row dict per observation in a parsed <Series> element."""
    attrs = dict(series_el.attrib)
    series_name = attrs.get("SERIES_NAME", "")
    freq_code = attrs.get("FREQ", "")
    short_desc = ""
    long_desc = ""

    for child in series_el:
        if _localname(child.tag) != "Annotations":
            continue
        for ann in child:
            atype = (ann.findtext("./{*}AnnotationType")
                     or _child_text(ann, "AnnotationType") or "")
            atext = (ann.findtext("./{*}AnnotationText")
                     or _child_text(ann, "AnnotationText") or "")
            low = atype.strip().lower()
            if low == "short description":
                short_desc = atext.strip()
            elif low == "long description":
                long_desc = atext.strip()

    attrs_json = json.dumps(attrs, sort_keys=True, ensure_ascii=False)

    for child in series_el:
        if _localname(child.tag) != "Obs":
            continue
        o = child.attrib
        yield {
            "release": release,
            "dataset_id": dataset_id,
            "series_name": series_name,
            "freq_code": freq_code,
            "frequency": _FREQ.get(freq_code, freq_code),
            "unit": attrs.get("UNIT"),
            "unit_mult": attrs.get("UNIT_MULT"),
            "currency": attrs.get("CURRENCY"),
            "short_description": short_desc,
            "long_description": long_desc,
            "series_attributes": attrs_json,
            "time_period": o.get("TIME_PERIOD"),
            "obs_value": _parse_obs_value(o.get("OBS_VALUE")),
            "obs_status": o.get("OBS_STATUS"),
        }


def _child_text(elem, localname):
    for c in elem:
        if _localname(c.tag) == localname:
            return c.text
    return None


def fetch_one(node_id: str) -> None:
    """Download + stream-parse one statistical release into raw parquet."""
    configure_http(headers={"User-Agent": _USER_AGENT})

    asset = node_id
    rel = node_id[len("federal-reserve-"):].upper()

    zip_bytes = _fetch_zip(rel)

    with zipfile.ZipFile(io.BytesIO(zip_bytes)) as zf:
        data_members = sorted(
            n for n in zf.namelist() if n.lower().endswith("_data.xml")
        )
        if not data_members:
            raise RuntimeError(
                f"rel={rel}: no *_data.xml in zip (members={zf.namelist()})"
            )

        total = 0
        batch: list[dict] = []
        with raw_parquet_writer(asset, SCHEMA) as writer:
            for data_name in data_members:
                with zf.open(data_name) as fh:
                    # iterparse streams decompression — the 590MB Z.1 XML is
                    # never fully resident. Clear each <Series> after reading it
                    # so only the current batch of rows lives in memory.
                    dataset_ids: list[str] = []
                    for event, elem in ET.iterparse(fh, events=("start", "end")):
                        name = _localname(elem.tag)
                        if event == "start":
                            if name == "DataSet":
                                dataset_ids.append(elem.attrib.get("id", ""))
                            continue
                        if name == "DataSet":
                            dataset_ids.pop()
                            elem.clear()
                            continue
                        if name != "Series":
                            continue
                        dataset_id = dataset_ids[-1] if dataset_ids else ""
                        for row in _series_rows(elem, rel, dataset_id):
                            batch.append(row)
                        elem.clear()
                        if len(batch) >= _BATCH_ROWS:
                            writer.write_table(
                                pa.Table.from_pylist(batch, schema=SCHEMA)
                            )
                            total += len(batch)
                            batch = []
            if batch:
                writer.write_table(pa.Table.from_pylist(batch, schema=SCHEMA))
                total += len(batch)

    if total == 0:
        raise RuntimeError(
            f"rel={rel}: parsed 0 observations from {', '.join(data_members)}"
        )
    print(f"  rel={rel}: wrote {total} observations")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"federal-reserve-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]


# One published Delta table per release. Uniform template: parse-and-type the
# raw observations, derive a DATE, drop missing values. Same shape every release
# because the raw schema is fixed across releases.
TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=f'''
            SELECT
                release,
                series_name,
                freq_code,
                frequency,
                unit,
                unit_mult,
                currency,
                short_description,
                long_description,
                series_attributes,
                time_period,
                TRY_CAST(time_period AS DATE) AS date,
                obs_value AS value,
                obs_status
            FROM "{s.id}"
            WHERE obs_value IS NOT NULL
        ''',
    )
    for s in DOWNLOAD_SPECS
]
