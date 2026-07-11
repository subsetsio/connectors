"""OpenAlex concepts — legacy concept hierarchy from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, join, short, stats


def _flat(r):
    ids = r.get("ids") or {}
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "description": r.get("description"),
        "level": r.get("level"),
        "wikidata": r.get("wikidata") or ids.get("wikidata"),
        "ancestors": join(short(a.get("id")) for a in (r.get("ancestors") or [])),
        "related_concepts": join(short(c.get("id")) for c in (r.get("related_concepts") or [])),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "h_index": stats(r, "h_index"),
        "i10_index": stats(r, "i10_index"),
        "mean_citedness": stats(r, "2yr_mean_citedness"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("concepts", _flat), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-concepts", fn=fetch, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-concepts-transform",
        deps=["openalex-concepts"],
        sql='''
            SELECT id, display_name, description,
                   CAST(level AS INTEGER) AS level,
                   wikidata, ancestors, related_concepts,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   CAST(h_index AS INTEGER)       AS h_index,
                   CAST(i10_index AS INTEGER)     AS i10_index,
                   CAST(mean_citedness AS DOUBLE) AS mean_citedness,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-concepts" WHERE id IS NOT NULL
        ''',
    ),
]
