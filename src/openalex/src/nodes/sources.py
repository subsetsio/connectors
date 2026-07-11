"""OpenAlex sources — reference entity table from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, join, short, stats


def _flat(r):
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "issn_l": r.get("issn_l"),
        "issn": join(r.get("issn")),
        "type": r.get("type"),
        "host_organization_name": r.get("host_organization_name"),
        "host_organization": short(r.get("host_organization")),
        "is_oa": r.get("is_oa"),
        "is_in_doaj": r.get("is_in_doaj"),
        "is_core": r.get("is_core"),
        "country_code": r.get("country_code"),
        "apc_usd": r.get("apc_usd"),
        "first_publication_year": r.get("first_publication_year"),
        "last_publication_year": r.get("last_publication_year"),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "h_index": stats(r, "h_index"),
        "i10_index": stats(r, "i10_index"),
        "mean_citedness": stats(r, "2yr_mean_citedness"),
        "created_date": r.get("created_date"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("sources", _flat), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-sources", fn=fetch, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-sources-transform",
        deps=["openalex-sources"],
        sql='''
            SELECT id, display_name, issn_l, issn, type,
                   host_organization_name, host_organization,
                   CAST(is_oa AS BOOLEAN)     AS is_oa,
                   CAST(is_in_doaj AS BOOLEAN) AS is_in_doaj,
                   CAST(is_core AS BOOLEAN)   AS is_core,
                   country_code,
                   CAST(apc_usd AS INTEGER)              AS apc_usd,
                   CAST(first_publication_year AS INTEGER) AS first_publication_year,
                   CAST(last_publication_year AS INTEGER)  AS last_publication_year,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   CAST(h_index AS INTEGER)       AS h_index,
                   CAST(i10_index AS INTEGER)     AS i10_index,
                   CAST(mean_citedness AS DOUBLE) AS mean_citedness,
                   TRY_CAST(created_date AS DATE)      AS created_date,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-sources" WHERE id IS NOT NULL
        ''',
    ),
]
