"""ParlGov connector — Parliament and Government Database (parties, elections,
cabinets for all EU + most OECD democracies, 1945-present).

Mechanism: bulk_csv. One stable CSV per table at
https://parlgov.fly.dev/data-csv/<table>/ (trailing slash; the server 301s the
unslashed form). The whole corpus is a few MB, so the shape is a stateless full
re-pull every run — no incremental query exists on the CSV path and the source
publishes revisions in place. Each table's full CSV is fetched, parsed, and
written as NDJSON with raw string cell values (empty string -> null); the SQL
transforms own all typing via explicit casts, which keeps the raw layer
schema-stable and pushes the correctness gate into DuckDB.
"""

import csv
import io


from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://parlgov.fly.dev/data-csv"

# Entity union — the rank-active ParlGov tables/views (see work/entity_union.json).
ENTITY_IDS = [
    "data_cabinet",
    "data_cabinet_party",
    "data_country",
    "data_election",
    "data_election_result",
    "data_party",
    "view_cabinet",
    "view_election",
    "view_party",
]


@transient_retry()
def _fetch_csv_text(table: str) -> str:
    resp = get(f"{BASE}/{table}/", timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.text


def fetch_one(node_id: str) -> None:
    asset = node_id  # runtime passes the spec id; it is also the asset name
    table = node_id[len("parlgov-"):].replace("-", "_")
    text = _fetch_csv_text(table)
    reader = csv.DictReader(io.StringIO(text))
    # Keep every cell as a raw string; collapse empty strings to null so the
    # transform's CAST sees real NULLs instead of failing on "".
    rows = [
        {k: (v if v not in ("", None) else None) for k, v in row.items()}
        for row in reader
    ]
    if not rows:
        raise AssertionError(f"{table}: CSV parsed to 0 rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"parlgov-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One thin parse-and-type SQL pass per table. Each reads its NDJSON view (all
# columns VARCHAR/null) and casts to the published schema. {src} is the dep view.
_TRANSFORM_SQL = {
    "parlgov-data-cabinet": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            name                              AS cabinet_name,
            CAST(start_date AS DATE)          AS start_date,
            CAST(termination_date AS DATE)    AS termination_date,
            caretaker = 'True'                AS caretaker,
            CAST(country_id AS INTEGER)       AS country_id,
            CAST(election_id AS INTEGER)      AS election_id,
            wikipedia,
            data_source
        FROM "{src}"
    """,
    "parlgov-data-cabinet-party": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            pm = 'True'                       AS prime_minister,
            defector = 'True'                 AS defector,
            party_id_source,
            CAST(cabinet_id AS INTEGER)       AS cabinet_id,
            CAST(party_id AS INTEGER)         AS party_id
        FROM "{src}"
    """,
    "parlgov-data-country": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            name                              AS country_name,
            name_short                        AS country_name_short,
            code_iso2,
            CAST(eu_accession_date AS DATE)   AS eu_accession_date,
            CAST(oecd_accession_date AS DATE) AS oecd_accession_date
        FROM "{src}"
    """,
    "parlgov-data-election": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            CAST(date AS DATE)                AS election_date,
            early = 'True'                    AS early,
            CAST(dissolution_date AS DATE)    AS dissolution_date,
            CAST(seats_total AS INTEGER)      AS seats_total,
            CAST(electorate AS BIGINT)        AS electorate,
            CAST(votes_cast AS BIGINT)        AS votes_cast,
            CAST(votes_valid AS BIGINT)       AS votes_valid,
            CAST(country_id AS INTEGER)       AS country_id,
            CAST(type_id AS INTEGER)          AS type_id,
            wikipedia
        FROM "{src}"
    """,
    "parlgov-data-election-result": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            party_id_source,
            CAST(seats AS INTEGER)            AS seats,
            CAST(vote_share AS DOUBLE)        AS vote_share,
            CAST(votes AS BIGINT)             AS votes,
            CAST(election_id AS INTEGER)      AS election_id,
            CAST(party_id AS INTEGER)         AS party_id,
            CAST(alliance_id AS INTEGER)      AS alliance_id
        FROM "{src}"
    """,
    "parlgov-data-party": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            name_short,
            name_english,
            name,
            name_ascii,
            wikipedia,
            CAST(foundation_date AS DATE)     AS foundation_date,
            CAST(dissolution_date AS DATE)    AS dissolution_date,
            CAST(country_id AS INTEGER)       AS country_id,
            CAST(family_id AS INTEGER)        AS family_id
        FROM "{src}"
    """,
    "parlgov-view-cabinet": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            country                           AS country_name_short,
            CAST(start_date AS DATE)          AS start_date,
            party                             AS party_name_short,
            pm = 'True'                       AS prime_minister,
            defector = 'True'                 AS defector,
            party_id_source,
            CAST(cabinet_id AS INTEGER)       AS cabinet_id,
            CAST(party_id AS INTEGER)         AS party_id
        FROM "{src}"
    """,
    "parlgov-view-election": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            country                           AS country_name_short,
            CAST(date AS DATE)                AS election_date,
            type                              AS election_type,
            party                             AS party_name_short,
            party_id_source,
            CAST(seats AS INTEGER)            AS seats,
            CAST(vote_share AS DOUBLE)        AS vote_share,
            CAST(votes AS BIGINT)             AS votes,
            CAST(election_id AS INTEGER)      AS election_id,
            CAST(party_id AS INTEGER)         AS party_id,
            CAST(alliance_id AS INTEGER)      AS alliance_id
        FROM "{src}"
    """,
    "parlgov-view-party": """
        SELECT
            CAST(id AS INTEGER)               AS id,
            country                           AS country_name_short,
            party_family,
            name_short,
            name_english,
            name,
            name_ascii,
            wikipedia,
            CAST(foundation_date AS DATE)     AS foundation_date,
            CAST(dissolution_date AS DATE)    AS dissolution_date
        FROM "{src}"
    """,
}

# Every table carries a unique integer `id` (its primary key). Only the cabinet
# and election tables have a genuine observation-period column; the party/country
# tables are timeless reference dimensions and get no temporal.
_TEMPORAL = {
    "parlgov-data-cabinet": "start_date",
    "parlgov-data-election": "election_date",
    "parlgov-view-cabinet": "start_date",
    "parlgov-view-election": "election_date",
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        key=("id",),
        temporal=_TEMPORAL.get(s.id),
        sql=_TRANSFORM_SQL[s.id].format(src=s.id),
    )
    for s in DOWNLOAD_SPECS
]
