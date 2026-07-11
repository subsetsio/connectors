"""OpenAlex domains — top level of the topic hierarchy from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, join, short


def _flat(r):
    ids = r.get("ids") or {}
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "description": r.get("description"),
        "wikidata": ids.get("wikidata"),
        "fields": join(short(f.get("id")) for f in (r.get("fields") or [])),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("domains", _flat), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-domains", fn=fetch, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-domains-transform",
        deps=["openalex-domains"],
        sql='''
            SELECT id, display_name, description, wikidata, fields,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-domains" WHERE id IS NOT NULL
        ''',
    ),
]
