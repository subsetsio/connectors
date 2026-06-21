"""OpenAlex SDGs — UN Sustainable Development Goals table from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, short


def _flat(r):
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "description": r.get("description"),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("sdgs", _flat), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-sdgs", fn=fetch, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-sdgs-transform",
        deps=["openalex-sdgs"],
        sql='''
            SELECT id, display_name, description,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-sdgs" WHERE id IS NOT NULL
        ''',
    ),
]
