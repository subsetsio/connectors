"""OpenAlex fields — taxonomy table from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, short


def _flat(r):
    dom = r.get("domain") or {}
    ids = r.get("ids") or {}
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "description": r.get("description"),
        "domain_id": short(dom.get("id")),
        "domain_name": dom.get("display_name"),
        "wikidata": ids.get("wikidata"),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("fields", _flat), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-fields", fn=fetch, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-fields-transform",
        deps=["openalex-fields"],
        sql='''
            SELECT id, display_name, description, domain_id, domain_name, wikidata,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-fields" WHERE id IS NOT NULL
        ''',
    ),
]
