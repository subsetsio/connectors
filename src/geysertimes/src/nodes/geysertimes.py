"""GeyserTimes (Yellowstone) download nodes."""

from __future__ import annotations

import gzip
import re
from urllib.parse import urljoin

import pyarrow as pa
import pyarrow.compute as pc
import pyarrow.csv as pv

from subsets_utils import NodeSpec, get, save_raw_parquet


ARCHIVE_URL = "https://geysertimes.org/archive/"
BASE_API = "https://www.geysertimes.org/api/v5"

ARCHIVE_HEADERS = {
    "User-Agent": "subsets.io geysertimes connector (contact: support@subsets.io)"
}

ERUPTION_SCHEMA = pa.schema(
    [
        ("eruption_id", pa.int64()),
        ("geyser_id", pa.int64()),
        ("geyser_name", pa.string()),
        ("eruption_time_epoch", pa.int64()),
        ("eruption_time", pa.timestamp("s", tz="UTC")),
        ("has_seconds", pa.bool_()),
        ("exact", pa.bool_()),
        ("near_start", pa.bool_()),
        ("in_eruption", pa.bool_()),
        ("electronic", pa.bool_()),
        ("approximate", pa.bool_()),
        ("webcam", pa.bool_()),
        ("initial", pa.bool_()),
        ("major", pa.bool_()),
        ("minor", pa.bool_()),
        ("questionable", pa.bool_()),
        ("duration_text", pa.string()),
        ("duration_seconds", pa.int64()),
        ("duration_resolution", pa.string()),
        ("duration_modifier", pa.string()),
        ("entrant", pa.string()),
        ("observer", pa.string()),
        ("eruption_comment", pa.string()),
        ("time_updated_epoch", pa.int64()),
        ("time_entered_epoch", pa.int64()),
        ("associated_primary_id", pa.int64()),
        ("other_comments", pa.string()),
    ]
)

GEYSER_SCHEMA = pa.schema(
    [
        ("geyser_id", pa.int64()),
        ("geyser_name", pa.string()),
        ("latitude", pa.float64()),
        ("longitude", pa.float64()),
        ("timezone", pa.string()),
        ("group_id", pa.int64()),
        ("group_name", pa.string()),
        ("server_update_epoch", pa.int64()),
    ]
)

ARCHIVE_TO_RAW = {
    "eruptionID": "eruption_id",
    "geyser": "geyser_name",
    "eruption_time_epoch": "eruption_time_epoch",
    "has_seconds": "has_seconds",
    "exact": "exact",
    "ns": "near_start",
    "ie": "in_eruption",
    "E": "electronic",
    "A": "approximate",
    "wc": "webcam",
    "ini": "initial",
    "maj": "major",
    "min": "minor",
    "q": "questionable",
    "duration": "duration_text",
    "duration_seconds": "duration_seconds",
    "duration_resolution": "duration_resolution",
    "duration_modifier": "duration_modifier",
    "entrant": "entrant",
    "observer": "observer",
    "eruption_comment": "eruption_comment",
    "time_updated": "time_updated_epoch",
    "time_entered": "time_entered_epoch",
    "associated_primaryID": "associated_primary_id",
    "other_comments": "other_comments",
}

GEYSER_TO_RAW = {
    "id": "geyser_id",
    "name": "geyser_name",
    "latitude": "latitude",
    "longitude": "longitude",
    "timezone": "timezone",
    "groupID": "group_id",
    "groupName": "group_name",
    "serverUpdate": "server_update_epoch",
}


def _latest_eruptions_url() -> str:
    resp = get(ARCHIVE_URL, headers=ARCHIVE_HEADERS, timeout=(10.0, 60.0))
    resp.raise_for_status()
    matches = re.findall(
        r"href=['\"](?P<href>\.?/complete/geysertimes_eruptions_complete_(?P<date>\d{4}-\d{2}-\d{2})\.tsv\.gz)['\"]",
        resp.text,
    )
    if not matches:
        raise RuntimeError("no complete eruptions archive link found")
    href, _date = max(matches, key=lambda item: item[1])
    return urljoin(ARCHIVE_URL, href)


def _read_archive_tsv(url: str) -> pa.Table:
    resp = get(url, headers=ARCHIVE_HEADERS, timeout=(10.0, 300.0))
    resp.raise_for_status()
    decompressed = gzip.decompress(resp.content)
    table = pv.read_csv(
        pa.BufferReader(decompressed),
        read_options=pv.ReadOptions(encoding="utf8"),
        parse_options=pv.ParseOptions(
            delimiter="\t",
            invalid_row_handler=lambda _row: "skip",
        ),
        convert_options=pv.ConvertOptions(
            strings_can_be_null=True,
            null_values=["", "NULL"],
            true_values=["1"],
            false_values=["0"],
            column_types={
                "eruptionID": pa.int64(),
                "geyser": pa.string(),
                "eruption_time_epoch": pa.int64(),
                "has_seconds": pa.bool_(),
                "exact": pa.bool_(),
                "ns": pa.bool_(),
                "ie": pa.bool_(),
                "E": pa.bool_(),
                "A": pa.bool_(),
                "wc": pa.bool_(),
                "ini": pa.bool_(),
                "maj": pa.bool_(),
                "min": pa.bool_(),
                "q": pa.bool_(),
                "duration": pa.string(),
                "duration_seconds": pa.int64(),
                "duration_resolution": pa.string(),
                "duration_modifier": pa.string(),
                "entrant": pa.string(),
                "observer": pa.string(),
                "eruption_comment": pa.string(),
                "time_updated": pa.int64(),
                "time_entered": pa.int64(),
                "associated_primaryID": pa.int64(),
                "other_comments": pa.string(),
            },
        ),
    )
    table = table.rename_columns([ARCHIVE_TO_RAW[name] for name in table.column_names])
    eruption_time = pc.cast(table["eruption_time_epoch"], pa.timestamp("s", tz="UTC"))
    idx = table.column_names.index("eruption_time_epoch") + 1
    return table.add_column(idx, "eruption_time", eruption_time)


def _to_int(value: str | None) -> int | None:
    return int(value) if value not in (None, "") else None


def _to_float(value: str | None) -> float | None:
    return float(value) if value not in (None, "") else None


def _fetch_geyser_rows() -> list[dict]:
    resp = get(f"{BASE_API}/geysers", timeout=(10.0, 60.0))
    resp.raise_for_status()
    data = resp.json()
    rows = []
    for rec in data.get("geysers", []):
        rows.append(
            {
                GEYSER_TO_RAW[key]: (
                    _to_int(value)
                    if key in {"id", "groupID", "serverUpdate"}
                    else _to_float(value)
                    if key in {"latitude", "longitude"}
                    else value
                )
                for key, value in rec.items()
                if key in GEYSER_TO_RAW
            }
        )
    return rows


def fetch_eruptions(node_id: str) -> None:
    """Fetch the latest nightly complete eruption archive."""
    table = _read_archive_tsv(_latest_eruptions_url())
    geyser_id_by_name = {
        row["geyser_name"]: row["geyser_id"] for row in _fetch_geyser_rows()
    }
    geyser_ids = pa.array(
        [geyser_id_by_name.get(name.as_py()) for name in table["geyser_name"]],
        type=pa.int64(),
    )
    table = table.add_column(1, "geyser_id", geyser_ids)
    save_raw_parquet(table.cast(ERUPTION_SCHEMA), node_id)


def fetch_geysers(node_id: str) -> None:
    """Fetch the geyser reference catalog from the public REST API."""
    rows = _fetch_geyser_rows()
    save_raw_parquet(pa.Table.from_pylist(rows, schema=GEYSER_SCHEMA), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="geysertimes-eruptions", fn=fetch_eruptions, kind="download"),
    NodeSpec(id="geysertimes-geysers", fn=fetch_geysers, kind="download"),
]
