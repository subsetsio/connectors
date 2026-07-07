from io import BytesIO

import pyarrow as pa
import pyarrow.parquet as pq
from subsets_utils import NodeSpec, get, save_raw_parquet


PREFIX = "scimago-journal-country-rank-"

ENTITY_CONFIG = {
    "journal-rankings": {
        "directory": "sjr-journal",
        "filename_prefix": "sjr_journals-",
        "schema": pa.schema(
            [
                ("year", pa.int64()),
                ("rank", pa.int64()),
                ("sourceid", pa.int64()),
                ("title", pa.string()),
                ("type", pa.string()),
                ("issn", pa.string()),
                ("publisher", pa.string()),
                ("open_access", pa.string()),
                ("open_access_diamond", pa.string()),
                ("sjr", pa.float64()),
                ("sjr_best_quartile", pa.string()),
                ("h_index", pa.int64()),
                ("total_docs_year", pa.int64()),
                ("total_docs_3years", pa.int64()),
                ("total_refs", pa.int64()),
                ("total_citations_3years", pa.int64()),
                ("citable_docs_3years", pa.int64()),
                ("citations_doc_2years", pa.float64()),
                ("ref_doc", pa.float64()),
                ("percent_female", pa.float64()),
                ("overton", pa.float64()),
                ("country", pa.string()),
                ("region", pa.string()),
                ("coverage", pa.string()),
                ("categories", pa.string()),
                ("areas", pa.string()),
            ]
        ),
    },
    "country-rankings": {
        "directory": "sjr-country",
        "filename_prefix": "sjr_countries-",
        "schema": pa.schema(
            [
                ("year", pa.int64()),
                ("rank", pa.int64()),
                ("country", pa.string()),
                ("region", pa.string()),
                ("documents", pa.int64()),
                ("citable_documents", pa.int64()),
                ("citations", pa.int64()),
                ("self_citations", pa.int64()),
                ("citations_per_document", pa.float64()),
                ("h_index", pa.int64()),
            ]
        ),
    },
}


def _year_from_name(name: str) -> int:
    stem = name.rsplit(".", 1)[0]
    return int(stem.rsplit("-", 1)[1])


def _latest_download_url(directory: str, filename_prefix: str) -> str:
    url = f"https://api.github.com/repos/ikashnitsky/sjrdata/contents/data-raw/{directory}?per_page=100"
    response = get(
        url,
        headers={"Accept": "application/vnd.github+json"},
        timeout=60.0,
    )
    response.raise_for_status()
    records = [
        record
        for record in response.json()
        if record.get("type") == "file"
        and record.get("name", "").startswith(filename_prefix)
        and record.get("name", "").endswith(".parquet")
    ]
    if not records:
        raise RuntimeError(f"No matching parquet files found in {directory}")
    latest = max(records, key=lambda record: _year_from_name(record["name"]))
    return latest["download_url"]


def _normalize_table(content: bytes, schema: pa.Schema) -> pa.Table:
    table = pq.read_table(BytesIO(content))
    missing = [field.name for field in schema if field.name not in table.column_names]
    if missing:
        raise RuntimeError(f"Source parquet missing expected columns: {missing}")
    table = table.select(schema.names)
    return table.cast(schema, safe=False)


def fetch_latest_parquet(asset_id: str) -> None:
    entity_id = asset_id.removeprefix(PREFIX)
    config = ENTITY_CONFIG[entity_id]
    url = _latest_download_url(config["directory"], config["filename_prefix"])
    response = get(url, timeout=180.0)
    response.raise_for_status()
    table = _normalize_table(response.content, config["schema"])
    save_raw_parquet(table, asset_id)


DOWNLOAD_SPECS = [
    NodeSpec(
        id="scimago-journal-country-rank-country-rankings",
        fn=fetch_latest_parquet,
    ),
    NodeSpec(
        id="scimago-journal-country-rank-journal-rankings",
        fn=fetch_latest_parquet,
    ),
]
