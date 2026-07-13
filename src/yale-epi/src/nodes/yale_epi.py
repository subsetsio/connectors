import io
import re
import urllib.request
import zipfile
from collections.abc import Iterable
from pathlib import PurePosixPath

import pandas as pd
import pyarrow as pa

from subsets_utils import NodeSpec, save_raw_ndjson, save_raw_parquet


BASE_URL = "https://epi.yale.edu/downloads/"
PREFIX = "yale-epi-"

FILES = {
    "2026-explanations-targets-weights": "epi2026methods2026-07-08.xlsx",
    "2026-indicator-scores": "epi2026indicatorsna.zip",
    "2026-indicator-scores-with-missing-value-codes": "epi2026indicatorsmvc.zip",
    "2026-raw-data": "epi2026rawdatana.zip",
    "2026-raw-data-with-missing-value-codes": "epi2026rawdatamvc.zip",
    "2026-scores-trends-and-ranks": "epi2026results2026-07-07.xlsx",
}

LONG_SCHEMA = pa.schema(
    [
        ("release_year", pa.int16()),
        ("source_file", pa.string()),
        ("variable_code", pa.string()),
        ("series_kind", pa.string()),
        ("country_code", pa.int64()),
        ("iso", pa.string()),
        ("country", pa.string()),
        ("observation_year", pa.int16()),
        ("value", pa.float64()),
        ("value_text", pa.string()),
        ("has_missing_value_codes", pa.bool_()),
        ("source_column", pa.string()),
    ]
)


def _entity_id(node_id: str) -> str:
    if not node_id.startswith(PREFIX):
        raise ValueError(f"unexpected node id {node_id!r}")
    entity_id = node_id.removeprefix(PREFIX)
    if entity_id not in FILES:
        raise KeyError(f"no download file configured for entity {entity_id!r}")
    return entity_id


def _fetch_bytes(filename: str) -> bytes:
    # Yale's edge currently returns 403 to httpx but accepts stdlib urllib.
    req = urllib.request.Request(
        BASE_URL + filename,
        headers={"User-Agent": "subsets-factory/1.0"},
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        return resp.read()


def _clean_name(value: object) -> str:
    text = str(value).strip().lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "unnamed"


def _dedupe_columns(columns: Iterable[object]) -> list[str]:
    counts: dict[str, int] = {}
    out = []
    for column in columns:
        base = _clean_name(column)
        counts[base] = counts.get(base, 0) + 1
        out.append(base if counts[base] == 1 else f"{base}_{counts[base]}")
    return out


def _json_ready(value: object) -> object:
    if pd.isna(value):
        return None
    if hasattr(value, "item"):
        return value.item()
    return value


def fetch_xlsx(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    filename = FILES[entity_id]
    content = _fetch_bytes(filename)
    workbook = pd.ExcelFile(io.BytesIO(content))
    rows = []
    for sheet_name in workbook.sheet_names:
        frame = pd.read_excel(workbook, sheet_name=sheet_name)
        frame.columns = _dedupe_columns(frame.columns)
        for idx, record in enumerate(frame.to_dict("records"), start=2):
            cleaned = {key: _json_ready(value) for key, value in record.items()}
            cleaned["release_year"] = 2026
            cleaned["source_file"] = filename
            cleaned["sheet_name"] = sheet_name
            cleaned["source_row_number"] = idx
            rows.append(cleaned)
    save_raw_ndjson(rows, node_id)


def _member_variable(name: str) -> tuple[str, str]:
    stem = PurePosixPath(name).name.removesuffix(".csv")
    match = re.match(r"(?P<code>[A-Z0-9]+)_(?P<kind>ind|raw)_", stem)
    if not match:
        raise ValueError(f"could not parse variable/kind from {name!r}")
    return match.group("code"), match.group("kind")


def _long_rows_from_csv(member_name: str, content: bytes, has_missing_codes: bool) -> list[dict]:
    frame = pd.read_csv(io.BytesIO(content))
    variable_code, series_kind = _member_variable(member_name)
    value_columns = [col for col in frame.columns if re.search(r"\.\d{4}$", str(col))]
    id_columns = [col for col in ("code", "iso", "country") if col in frame.columns]
    long = frame.melt(
        id_vars=id_columns,
        value_vars=value_columns,
        var_name="source_column",
        value_name="value",
    )
    long["release_year"] = 2026
    long["source_file"] = PurePosixPath(member_name).name
    long["variable_code"] = variable_code
    long["series_kind"] = series_kind
    long["country_code"] = pd.to_numeric(long.get("code"), errors="coerce").astype("Int64")
    long["observation_year"] = long["source_column"].str.extract(r"\.(\d{4})$")[0].astype("Int64")
    long["value_text"] = long["value"].map(lambda value: None if pd.isna(value) else str(value))
    long["value"] = pd.to_numeric(long["value"], errors="coerce")
    long["has_missing_value_codes"] = has_missing_codes
    long = long.rename(columns={"code": "drop_code"})
    keep = [field.name for field in LONG_SCHEMA]
    out = long[keep].where(pd.notna(long[keep]), None)
    for column in ("source_file", "variable_code", "series_kind", "iso", "country", "value_text", "source_column"):
        out[column] = out[column].map(lambda value: None if value is None else str(value))
    for column in ("release_year", "country_code", "observation_year"):
        out[column] = out[column].map(lambda value: None if value is None else int(value))
    out["value"] = out["value"].map(lambda value: None if value is None else float(value))
    out["has_missing_value_codes"] = out["has_missing_value_codes"].map(bool)
    return out.to_dict("records")


def fetch_zip_csvs(node_id: str) -> None:
    entity_id = _entity_id(node_id)
    filename = FILES[entity_id]
    has_missing_codes = "missing-value-codes" in entity_id
    content = _fetch_bytes(filename)
    rows = []
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for member_name in sorted(archive.namelist()):
            if member_name.lower().endswith(".csv"):
                rows.extend(_long_rows_from_csv(member_name, archive.read(member_name), has_missing_codes))
    table = pa.Table.from_pylist(rows, schema=LONG_SCHEMA)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="yale-epi-2026-explanations-targets-weights", fn=fetch_xlsx),
    NodeSpec(id="yale-epi-2026-indicator-scores", fn=fetch_zip_csvs),
    NodeSpec(id="yale-epi-2026-indicator-scores-with-missing-value-codes", fn=fetch_zip_csvs),
    NodeSpec(id="yale-epi-2026-raw-data", fn=fetch_zip_csvs),
    NodeSpec(id="yale-epi-2026-raw-data-with-missing-value-codes", fn=fetch_zip_csvs),
    NodeSpec(id="yale-epi-2026-scores-trends-and-ranks", fn=fetch_xlsx),
]
