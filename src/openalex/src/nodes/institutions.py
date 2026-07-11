"""OpenAlex institutions — reference entity table from the S3 snapshot."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import iter_entity_rows, short, stats


def _flat(r):
    geo = r.get("geo") or {}
    return {
        "id": short(r.get("id")),
        "display_name": r.get("display_name"),
        "ror": r.get("ror"),
        "type": r.get("type"),
        "country_code": r.get("country_code"),
        "homepage_url": r.get("homepage_url"),
        "city": geo.get("city"),
        "region": geo.get("region"),
        "geo_country": geo.get("country"),
        "latitude": geo.get("latitude"),
        "longitude": geo.get("longitude"),
        "works_count": r.get("works_count"),
        "cited_by_count": r.get("cited_by_count"),
        "h_index": stats(r, "h_index"),
        "i10_index": stats(r, "i10_index"),
        "mean_citedness": stats(r, "2yr_mean_citedness"),
        "created_date": r.get("created_date"),
        "updated_date": r.get("updated_date"),
    }


def fetch(node_id: str) -> None:
    save_raw_ndjson(iter_entity_rows("institutions", _flat), node_id)


_DOWNLOAD_SPECS = [
    NodeSpec(id="openalex-institutions", fn=fetch, kind="download"),
]

_TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="openalex-institutions-transform",
        deps=["openalex-institutions"],
        sql='''
            SELECT id, display_name, ror, type, country_code, homepage_url,
                   city, region, geo_country,
                   CAST(latitude AS DOUBLE)  AS latitude,
                   CAST(longitude AS DOUBLE) AS longitude,
                   CAST(works_count AS BIGINT)    AS works_count,
                   CAST(cited_by_count AS BIGINT) AS cited_by_count,
                   CAST(h_index AS INTEGER)       AS h_index,
                   CAST(i10_index AS INTEGER)     AS i10_index,
                   CAST(mean_citedness AS DOUBLE) AS mean_citedness,
                   TRY_CAST(created_date AS DATE)      AS created_date,
                   TRY_CAST(updated_date AS TIMESTAMP) AS updated_at
            FROM "openalex-institutions" WHERE id IS NOT NULL
        ''',
    ),
]
