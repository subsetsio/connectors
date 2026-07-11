"""OpenAlex keywords — keyword vocabulary from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, short


def _flat(r):
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("keywords", _flat), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-keywords", fn=fetch, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-keywords-transform",
        deps=["openalex-keywords"],
        sql='''
            SELECT id, display_name,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-keywords" WHERE id IS NOT NULL
        ''',
    ),
]
