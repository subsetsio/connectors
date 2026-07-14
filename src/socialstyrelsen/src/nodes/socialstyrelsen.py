import csv
import json
import os
import re
import shutil
import tempfile
import unicodedata
import zipfile
from datetime import datetime, timezone
from pathlib import Path

import duckdb

from subsets_utils import (
    MaintainSpec,
    NodeSpec,
    configure_http,
    get,
    get_client,
    raw_asset_exists,
    raw_writer,
    record_source_signature,
    source_unchanged,
)

from constants import ENTITY_IDS, SUBJECT_NAMES


BASE_URL = "https://sdb.socialstyrelsen.se/api/v1/sv"
PAGE_SIZE = 5000
SLUG = "socialstyrelsen"
BULK_EXT = "parquet"
REST_EXT = "ndjson.gz"
ZIP_TIMEOUT_S = 1800.0

BULK_URLS = {
    "dodsorsaker": "https://sdb.socialstyrelsen.se/export/csv/statistikdatabasen-dodsorsaker.zip",
    "graviditeterforlossningarochnyfodda": (
        "https://sdb.socialstyrelsen.se/export/csv/"
        "statistikdatabasen-graviditeter%2c forlossningar och nyfodda.zip"
    ),
    "lakemedel": "https://sdb.socialstyrelsen.se/export/csv/statistikdatabasen-lakemedel.zip",
    "yttreorsakertillskadorochforgiftningar": (
        "https://sdb.socialstyrelsen.se/export/csv/"
        "statistikdatabasen-yttre orsaker till skador och forgiftningar - vuxna.zip"
    ),
    "yttreorsakertillskadorochforgiftningarbarn": (
        "https://sdb.socialstyrelsen.se/export/csv/"
        "statistikdatabasen-yttre orsaker till skador och forgiftningar - barn.zip"
    ),
}


def _fetched_at() -> str:
    return datetime.now(timezone.utc).isoformat()


def _entity_from_node_id(node_id: str) -> str:
    prefix = f"{SLUG}-"
    if not node_id.startswith(prefix):
        raise ValueError(f"unexpected node id {node_id!r}")
    return node_id.removeprefix(prefix).replace("-", "_")


def _get_json(url: str, *, params: dict | None = None):
    resp = get(url, params=params, timeout=180.0)
    resp.raise_for_status()
    return resp.json()


def _dimension_values(entity_id: str, dimension_id: str) -> list[dict]:
    values = _get_json(f"{BASE_URL}/{entity_id}/{dimension_id}")
    if not isinstance(values, list):
        raise ValueError(f"{entity_id}/{dimension_id}: expected list, got {type(values).__name__}")
    return values


def _value_key(dimension_id: str) -> str:
    return "ar" if dimension_id == "ar" else f"{dimension_id}Id"


def _build_dimension_maps(entity_id: str) -> tuple[list[dict], dict[str, dict[str, str]]]:
    dimensions = _get_json(f"{BASE_URL}/{entity_id}")
    if not isinstance(dimensions, list) or not dimensions:
        raise ValueError(f"{entity_id}: expected non-empty dimension list")

    label_maps: dict[str, dict[str, str]] = {}
    for dim in dimensions:
        dim_id = dim.get("namn")
        if not dim_id:
            continue
        values = _dimension_values(entity_id, dim_id)
        labels = {}
        for value in values:
            key = value.get("id", value.get("kod", value.get("text")))
            if key is None:
                continue
            labels[str(key)] = value.get("text")
        label_maps[dim_id] = labels
    return dimensions, label_maps


def _metric_ids(label_maps: dict[str, dict[str, str]]) -> list[str | None]:
    metric_map = label_maps.get("matt")
    if not metric_map:
        return [None]
    return list(metric_map.keys())


def _result_url(entity_id: str, metric_id: str | None) -> str:
    if metric_id is None:
        return f"{BASE_URL}/{entity_id}/resultat"
    return f"{BASE_URL}/{entity_id}/resultat/matt/{metric_id}"


def _label_specs(dimensions: list[dict], label_maps: dict[str, dict[str, str]]) -> list[tuple[str, str, dict[str, str]]]:
    specs = []
    for dim in dimensions:
        dim_id = dim.get("namn")
        if not dim_id:
            continue
        labels = label_maps.get(dim_id) or {}
        if labels:
            specs.append((_value_key(dim_id), f"{dim_id}Text", labels))
    return specs


def _enrich_rest_row(
    row: dict,
    *,
    entity_id: str,
    subject_name: str,
    label_specs: list[tuple[str, str, dict[str, str]]],
    fetched_at: str,
) -> dict:
    out = {
        "subject_id": entity_id,
        "subject_name": subject_name,
        "fetched_at": fetched_at,
    }
    out.update(row)
    for key, text_key, labels in label_specs:
        value = row.get(key)
        if value is None:
            continue
        label = labels.get(str(value))
        if label is not None:
            out[text_key] = label
    return out


def _download_zip(url: str) -> tuple[Path, object]:
    configure_http(timeout=ZIP_TIMEOUT_S)
    client = get_client()
    fd, path_str = tempfile.mkstemp(prefix="socialstyrelsen-", suffix=".zip")
    os.close(fd)
    path = Path(path_str)
    response = None
    try:
        with client.stream("GET", url, timeout=ZIP_TIMEOUT_S, follow_redirects=True) as resp:
            response = resp
            resp.raise_for_status()
            with path.open("wb") as out:
                for chunk in resp.iter_bytes(chunk_size=1024 * 1024):
                    if chunk:
                        out.write(chunk)
    except Exception:
        path.unlink(missing_ok=True)
        raise
    return path, response


def _clean_key(value: str | None) -> str:
    text = unicodedata.normalize("NFKD", value or "")
    text = text.encode("ascii", "ignore").decode("ascii").lower()
    text = re.sub(r"[^a-z0-9]+", "_", text).strip("_")
    return text or "unnamed"


def _coerce_value(key: str, value: str | None):
    if value is None:
        return None
    text = value.strip()
    if text == "":
        return None
    if key == "ar" and re.fullmatch(r"\d{4}", text):
        return int(text)
    return text


def _sql_str(value: str) -> str:
    return "'" + value.replace("'", "''") + "'"


def _iter_zip_csvs(path: Path):
    with zipfile.ZipFile(path) as zf:
        for info in zf.infolist():
            name = info.filename
            lower = name.lower()
            if info.is_dir() or not lower.endswith(".csv") or " - data - " not in lower:
                continue
            with zf.open(info) as raw:
                text = (line.decode("utf-8-sig") for line in raw)
                reader = csv.DictReader(text, delimiter=";")
                if not reader.fieldnames:
                    continue
                key_counts: dict[str, int] = {}
                keys = []
                for field in reader.fieldnames:
                    key = _clean_key(field)
                    seen = key_counts.get(key, 0)
                    key_counts[key] = seen + 1
                    keys.append(key if seen == 0 else f"{key}_{seen + 1}")
                yield name, reader.fieldnames, keys, reader


def _write_clean_csvs(path: Path, directory: Path) -> tuple[int, list[str]]:
    rows_written = 0
    columns = ["source_file"]
    seen_columns = set(columns)

    for index, (name, fieldnames, keys, reader) in enumerate(_iter_zip_csvs(path)):
        for key in keys:
            if key not in seen_columns:
                columns.append(key)
                seen_columns.add(key)

        out_path = directory / f"part-{index:05d}.csv"
        with out_path.open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=["source_file", *keys], extrasaction="ignore")
            writer.writeheader()
            for row in reader:
                out_row = {"source_file": name}
                for original, key in zip(fieldnames, keys, strict=False):
                    out_row[key] = _coerce_value(key, row.get(original))
                writer.writerow(out_row)
                rows_written += 1

    return rows_written, columns


def _clean_csvs_to_parquet(
    directory: Path,
    parquet_path: Path,
    *,
    columns: list[str],
    entity_id: str,
    subject_name: str,
    fetched_at: str,
) -> None:
    select_exprs = []
    for column in columns:
        quoted = '"' + column.replace('"', '""') + '"'
        if column == "ar":
            select_exprs.append(f"TRY_CAST({quoted} AS BIGINT) AS {quoted}")
        else:
            select_exprs.append(f"CAST({quoted} AS VARCHAR) AS {quoted}")
    select_exprs.extend(
        [
            f"{_sql_str(entity_id)} AS subject_id",
            f"{_sql_str(subject_name)} AS subject_name",
            f"{_sql_str(fetched_at)} AS fetched_at",
        ]
    )

    con = duckdb.connect()
    try:
        con.execute(
            f"""
            COPY (
                SELECT {", ".join(select_exprs)}
                FROM read_csv_auto(
                    {_sql_str(str(directory / "*.csv"))},
                    header=true,
                    all_varchar=true,
                    union_by_name=true,
                    sample_size=-1
                )
            )
            TO {_sql_str(str(parquet_path))} (FORMAT PARQUET, COMPRESSION ZSTD)
            """
        )
    finally:
        con.close()


def _write_json_line(out, row: dict) -> None:
    out.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")))
    out.write("\n")


def _fetch_rest_subject(node_id: str, entity_id: str, subject_name: str) -> int:
    dimensions, label_maps = _build_dimension_maps(entity_id)
    label_specs = _label_specs(dimensions, label_maps)
    fetched_at = _fetched_at()
    rows_written = 0

    with raw_writer(node_id, REST_EXT, mode="wt", compression="gzip") as out:
        for metric_id in _metric_ids(label_maps):
            url = _result_url(entity_id, metric_id)
            first = _get_json(url, params={"per_sida": PAGE_SIZE, "sida": 1})
            first_rows = first.get("data")
            if not isinstance(first_rows, list):
                raise ValueError(f"{entity_id}: page 1 returned no data list")

            total_pages = int(first.get("sidor") or 1)
            for page in range(1, total_pages + 1):
                if page == 1:
                    rows = first_rows
                else:
                    data = _get_json(url, params={"per_sida": PAGE_SIZE, "sida": page})
                    rows = data.get("data")
                    if not isinstance(rows, list):
                        raise ValueError(f"{entity_id}: page {page} returned no data list")
                for row in rows:
                    _write_json_line(
                        out,
                        _enrich_rest_row(
                            row,
                            entity_id=entity_id,
                            subject_name=subject_name,
                            label_specs=label_specs,
                            fetched_at=fetched_at,
                        ),
                    )
                    rows_written += 1
    return rows_written


def _fetch_bulk_subject(node_id: str, entity_id: str, subject_name: str, url: str) -> int:
    fetched_at = _fetched_at()
    path, response = _download_zip(url)
    tmpdir = Path(tempfile.mkdtemp(prefix=f"{node_id}-"))
    try:
        csv_dir = tmpdir / "csv"
        csv_dir.mkdir()
        parquet_path = tmpdir / "data.parquet"
        rows_written, columns = _write_clean_csvs(path, csv_dir)
        if rows_written == 0:
            raise AssertionError(f"{node_id}: fetched zero result rows from bulk ZIP")
        _clean_csvs_to_parquet(
            csv_dir,
            parquet_path,
            columns=columns,
            entity_id=entity_id,
            subject_name=subject_name,
            fetched_at=fetched_at,
        )
        with parquet_path.open("rb") as src, raw_writer(node_id, BULK_EXT, mode="wb") as out:
            shutil.copyfileobj(src, out, length=1024 * 1024)
        record_source_signature(node_id, url, response=response)
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)
        path.unlink(missing_ok=True)
    return rows_written


def fetch_subject(node_id: str) -> None:
    entity_id = _entity_from_node_id(node_id)
    if entity_id not in ENTITY_IDS:
        raise ValueError(f"{node_id}: unknown entity {entity_id!r}")

    subject_name = SUBJECT_NAMES.get(entity_id, entity_id)
    if entity_id in BULK_URLS:
        rows_written = _fetch_bulk_subject(node_id, entity_id, subject_name, BULK_URLS[entity_id])
    else:
        rows_written = _fetch_rest_subject(node_id, entity_id, subject_name)

    if rows_written == 0:
        raise AssertionError(f"{node_id}: fetched zero result rows")
    print(f"  -> {node_id}: wrote {rows_written:,} rows")


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        fn=fetch_subject,
        kind="download",
    )
    for entity_id in ENTITY_IDS
]

MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id=f"{SLUG}-{entity_id.lower().replace('_', '-')}",
        description="Bulk CSV ZIP updated by Socialstyrelsen developer exports; checked via Last-Modified",
        check=lambda asset_id, url=url: source_unchanged(asset_id, url) and raw_asset_exists(asset_id, BULK_EXT),
    )
    for entity_id, url in BULK_URLS.items()
]
