"""EPO technology-field metadata (fields-metadata.json)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import fetch_json


def fetch_fields(node_id: str) -> None:
    """fields-metadata.json: a flat list of technology-field records."""
    data = fetch_json("fields-metadata.json")
    save_raw_ndjson(data, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="epo-fields", fn=fetch_fields, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="epo-fields-transform",
        deps=["epo-fields"],
        sql='''
            SELECT
                CAST(field_id AS INTEGER)   AS field_id,
                field_name,
                field_sector_id,
                CAST(field_rank AS INTEGER) AS field_rank
            FROM "epo-fields"
        ''',
    ),
]
