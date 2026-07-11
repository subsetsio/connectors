"""OpenAlex topics — taxonomy table from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, join, short


def _flat(r):
    dom = r.get("domain") or {}
    fld = r.get("field") or {}
    sub = r.get("subfield") or {}
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "description": r.get("description"),
        "domain_id": short(dom.get("id")),
        "domain_name": dom.get("display_name"),
        "field_id": short(fld.get("id")),
        "field_name": fld.get("display_name"),
        "subfield_id": short(sub.get("id")),
        "subfield_name": sub.get("display_name"),
        "keywords": join(r.get("keywords")),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("topics", _flat), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-topics", fn=fetch, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-topics-transform",
        deps=["openalex-topics"],
        sql='''
            SELECT id, display_name, description,
                   domain_id, domain_name, field_id, field_name,
                   subfield_id, subfield_name, keywords,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-topics" WHERE id IS NOT NULL
        ''',
    ),
]
