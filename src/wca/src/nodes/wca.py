"""WCA public results export downloads.

The WCA publishes one daily TSV zip containing all public results tables. The
runtime requires one NodeSpec per accepted table, but downloading the same large
zip once per table would be wasteful. The first node materializes every table in
the zip; dependent table nodes then verify their raw parquet asset exists. If a
dependent node is retried in isolation, it materializes the full export again.
"""

from __future__ import annotations

import tempfile
import zipfile
from pathlib import Path

import pyarrow as pa
import pyarrow.csv as pacsv

from subsets_utils import NodeSpec, get, raw_asset_exists, raw_parquet_writer

EXPORT_METADATA_URL = "https://www.worldcubeassociation.org/api/v0/export/public"
BOOTSTRAP_SPEC_ID = "wca-championships"

TABLE_BY_SPEC_ID = {
    "wca-championships": "championships",
    "wca-competitions": "competitions",
    "wca-continents": "continents",
    "wca-countries": "countries",
    "wca-eligible-country-iso2s-for-championship": "eligible_country_iso2s_for_championship",
    "wca-events": "events",
    "wca-formats": "formats",
    "wca-persons": "persons",
    "wca-ranks-average": "ranks_average",
    "wca-ranks-single": "ranks_single",
    "wca-result-attempts": "result_attempts",
    "wca-results": "results",
    "wca-round-types": "round_types",
    "wca-scrambles": "scrambles",
}


def _export_metadata() -> dict:
    resp = get(EXPORT_METADATA_URL, timeout=(10.0, 60.0))
    resp.raise_for_status()
    return resp.json()


def _download_zip(url: str) -> Path:
    resp = get(url, timeout=(30.0, 900.0))
    resp.raise_for_status()
    tmp = tempfile.NamedTemporaryFile(prefix="wca-export-", suffix=".tsv.zip", delete=False)
    try:
        tmp.write(resp.content)
        return Path(tmp.name)
    finally:
        tmp.close()


def _schema_for(header: list[str]) -> pa.Schema:
    fields = [(col, pa.string()) for col in header]
    fields.extend([
        ("_source_table", pa.string()),
        ("_export_date", pa.string()),
        ("_export_version", pa.string()),
    ])
    return pa.schema(fields)


def _write_tsv_member(
    zf: zipfile.ZipFile,
    *,
    table_id: str,
    asset_id: str,
    export_date: str,
    export_version: str,
) -> None:
    member = f"WCA_export_{table_id}.tsv"
    with zf.open(member) as f:
        header = f.readline().decode("utf-8").rstrip("\r\n").split("\t")

    schema = _schema_for(header)
    convert = pacsv.ConvertOptions(
        column_types={col: pa.string() for col in header},
        strings_can_be_null=True,
    )
    parse = pacsv.ParseOptions(delimiter="\t", newlines_in_values=True)
    read = pacsv.ReadOptions(block_size=8 * 1024 * 1024)

    rows = 0
    with zf.open(member) as f, raw_parquet_writer(asset_id, schema) as writer:
        reader = pacsv.open_csv(
            f,
            read_options=read,
            parse_options=parse,
            convert_options=convert,
        )
        for batch in reader:
            n = batch.num_rows
            rows += n
            batch = batch.append_column(
                "_source_table",
                pa.array([table_id] * n, type=pa.string()),
            )
            batch = batch.append_column(
                "_export_date",
                pa.array([export_date] * n, type=pa.string()),
            )
            batch = batch.append_column(
                "_export_version",
                pa.array([export_version] * n, type=pa.string()),
            )
            writer.write_batch(batch)
    if rows == 0:
        raise RuntimeError(f"{member} contained no data rows")
    print(f"WCA: wrote {asset_id} from {member}: {rows:,} rows")


def _materialize_all_tables() -> None:
    metadata = _export_metadata()
    zip_path = _download_zip(metadata["tsv_url"])
    try:
        with zipfile.ZipFile(zip_path) as zf:
            names = set(zf.namelist())
            for asset_id, table_id in TABLE_BY_SPEC_ID.items():
                member = f"WCA_export_{table_id}.tsv"
                if member not in names:
                    raise FileNotFoundError(f"{member} not found in WCA export zip")
                _write_tsv_member(
                    zf,
                    table_id=table_id,
                    asset_id=asset_id,
                    export_date=metadata.get("export_date"),
                    export_version=metadata.get("export_version"),
                )
    finally:
        zip_path.unlink(missing_ok=True)


def fetch_table(node_id: str) -> None:
    if node_id not in TABLE_BY_SPEC_ID:
        raise ValueError(f"unknown WCA table spec id: {node_id}")
    if raw_asset_exists(node_id, "parquet"):
        print(f"WCA: {node_id} already materialized by the bootstrap node")
        return
    _materialize_all_tables()
    if not raw_asset_exists(node_id, "parquet"):
        raise RuntimeError(f"{node_id} was not materialized from the WCA export")


DOWNLOAD_SPECS = [
    NodeSpec(id="wca-championships", fn=fetch_table, kind="download"),
    NodeSpec(id="wca-competitions", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-continents", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-countries", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-eligible-country-iso2s-for-championship", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-events", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-formats", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-persons", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-ranks-average", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-ranks-single", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-result-attempts", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-results", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-round-types", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
    NodeSpec(id="wca-scrambles", fn=fetch_table, kind="download", deps=(BOOTSTRAP_SPEC_ID,)),
]
