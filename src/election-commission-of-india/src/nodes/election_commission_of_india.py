"""Election Commission of India — 2024 Lok Sabha General Election tables.

Source: data.gov.in Open Government Data (OGD) Platform, organization
"Election Commission of India". Five tabular resources are pulled, one
download NodeSpec each, via the OGD REST API
(https://api.data.gov.in/resource/{index_name}).

Fetch shape: stateless full re-pull. Each resource is tens-to-hundreds of
rows, so we re-fetch the whole table every run and overwrite — no watermark,
no incremental (the API exposes no `since`/cursor filter; resources are
republished wholesale, not appended). Auth is an `api-key` query param; the
public OGD sample key is the default, overridable via DATA_GOV_IN_API_KEY.
The sample key caps each page at 10 records, so we paginate by offset until
the `total` reported on the first page is reached.

Raw is saved as NDJSON with every value stringified, because the OGD API
returns mixed JSON types within a column (e.g. 0 and "0"); the transform SQL
re-types each column with TRY_CAST, which is the single source of truth for
column types.
"""

import os

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson, transient_retry

from constants import ENTITY_IDS

SLUG = "election-commission-of-india"
BASE = "https://api.data.gov.in/resource/"
DEMO_KEY = "579b464db66ec23bdd000001cdd3946e44ce4aad7209ff7b23ac571b"
PAGE = 100          # demo key silently caps to 10; a registered key honours larger
MAX_PAGES = 1000    # safety ceiling — raises (never silently returns) on hit


def _api_key() -> str:
    return os.environ.get("DATA_GOV_IN_API_KEY", DEMO_KEY)


def _dl_id(entity_id: str) -> str:
    return f"{SLUG}-{entity_id.lower().replace('_', '-')}"


@transient_retry()
def _fetch_page(resource_id: str, offset: int) -> dict:
    resp = get(
        BASE + resource_id,
        params={
            "format": "json",
            "limit": str(PAGE),
            "offset": str(offset),
            "api-key": _api_key(),
        },
        timeout=(10.0, 120.0),
    )
    resp.raise_for_status()
    return resp.json()


def fetch_one(node_id: str) -> None:
    asset = node_id                         # the spec id IS the asset name
    resource_id = node_id[len(SLUG) + 1:]   # strip "election-commission-of-india-"
    rows: list = []
    offset = 0
    total = None
    pages = 0
    while True:
        if pages >= MAX_PAGES:
            raise RuntimeError(
                f"{asset}: exceeded MAX_PAGES={MAX_PAGES} (offset={offset}, total={total})"
            )
        d = _fetch_page(resource_id, offset)
        if total is None:
            total = int(d.get("total") or 0)
        recs = d.get("records") or []
        if not recs:
            break
        rows.extend(recs)
        pages += 1
        offset += len(recs)
        if total and offset >= total:
            break
    # Stringify every value: the OGD API mixes int/float/str within a column,
    # so a uniform VARCHAR raw lets the transform own typing via TRY_CAST.
    norm = [{k: (None if v is None else str(v)) for k, v in r.items()} for r in rows]
    save_raw_ndjson(norm, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=_dl_id(eid), fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]


# --- Transforms: one published Delta table per resource ---------------------

_ELECTORS = _dl_id("1a0a8469-9e7e-4cc7-9f20-5f16ab973cbd")
_SUCCESSFUL = _dl_id("194d454f-3ea8-4621-a915-b211c66e46a7")
_CANDIDATES = _dl_id("0bd877c0-031d-49da-a743-d102dec6e7b7")
_PC_HIGHLIGHTS = _dl_id("a27ba4e9-73c2-40d1-90b2-41d71ea7c283")
_VOTERS = _dl_id("f7f1bf09-7633-4474-96b2-62630c70f33c")

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{_ELECTORS}-transform",
        deps=[_ELECTORS],
        sql=f'''
            SELECT
                CAST(state_ut AS VARCHAR)                          AS state_ut,
                TRY_CAST(general_including_nris____m     AS BIGINT) AS electors_general_male,
                TRY_CAST(general_including_nris____f     AS BIGINT) AS electors_general_female,
                TRY_CAST(general_including_nris____tg    AS BIGINT) AS electors_general_third_gender,
                TRY_CAST(general_including_nris____total AS BIGINT) AS electors_general_total,
                TRY_CAST(service___m     AS BIGINT)                 AS electors_service_male,
                TRY_CAST(service___f     AS BIGINT)                 AS electors_service_female,
                TRY_CAST(service___total AS BIGINT)                 AS electors_service_total,
                TRY_CAST(grand___m     AS BIGINT)                   AS electors_grand_male,
                TRY_CAST(grand___f     AS BIGINT)                   AS electors_grand_female,
                TRY_CAST(grand___tg    AS BIGINT)                   AS electors_grand_third_gender,
                TRY_CAST(grand___total AS BIGINT)                   AS electors_grand_total,
                TRY_CAST(nris___m     AS BIGINT)                    AS electors_nri_male,
                TRY_CAST(nris___f     AS BIGINT)                    AS electors_nri_female,
                TRY_CAST(nris___tg    AS BIGINT)                    AS electors_nri_third_gender,
                TRY_CAST(nris___total AS BIGINT)                    AS electors_nri_total
            FROM "{_ELECTORS}"
            WHERE state_ut IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_VOTERS}-transform",
        deps=[_VOTERS],
        sql=f'''
            SELECT
                CAST(state_name AS VARCHAR)                AS state_name,
                CAST(constituency_type AS VARCHAR)         AS constituency_type,
                TRY_CAST(no_of_seats AS BIGINT)            AS no_of_seats,
                TRY_CAST(electors___male AS BIGINT)        AS electors_male,
                TRY_CAST(electors___female AS BIGINT)      AS electors_female,
                TRY_CAST(electors___third_gender AS BIGINT) AS electors_third_gender,
                TRY_CAST(electors___total AS BIGINT)       AS electors_total,
                TRY_CAST(electors___nris AS BIGINT)        AS electors_nris,
                TRY_CAST(electors___service AS BIGINT)     AS electors_service,
                TRY_CAST(voters___male AS BIGINT)          AS voters_male,
                TRY_CAST(voters___female AS BIGINT)        AS voters_female,
                TRY_CAST(voters___third_gender AS BIGINT)  AS voters_third_gender,
                TRY_CAST(voters___postal AS BIGINT)        AS voters_postal,
                TRY_CAST(voters___total AS BIGINT)         AS voters_total,
                TRY_CAST(voters___nris AS BIGINT)          AS voters_nris,
                TRY_CAST(voters___poll__ AS DOUBLE)        AS voter_turnout_pct,
                TRY_CAST(rejected_votes__postal_ AS BIGINT) AS rejected_votes_postal,
                TRY_CAST(evm_rejected_votes AS BIGINT)     AS evm_rejected_votes,
                TRY_CAST(nota_votes AS BIGINT)             AS nota_votes,
                TRY_CAST(valid_votes_polled AS BIGINT)     AS valid_votes_polled,
                TRY_CAST(tendered_votes AS BIGINT)         AS tendered_votes
            FROM "{_VOTERS}"
            WHERE state_name IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_CANDIDATES}-transform",
        deps=[_CANDIDATES],
        sql=f'''
            SELECT
                CAST(state_ut AS VARCHAR)                                            AS state_ut,
                TRY_CAST(no__of_seats AS BIGINT)                                     AS no_of_seats,
                TRY_CAST(constituencies_with_candidates_numbering____1____15 AS BIGINT)  AS constituencies_candidates_1_15,
                TRY_CAST(constituencies_with_candidates_numbering____15____31 AS BIGINT) AS constituencies_candidates_15_31,
                TRY_CAST(constituencies_with_candidates_numbering____31____47 AS BIGINT) AS constituencies_candidates_31_47,
                TRY_CAST(constituencies_with_candidates_numbering____47____63 AS BIGINT) AS constituencies_candidates_47_63,
                TRY_CAST(constituencies_with_candidates_numbering____63 AS BIGINT)       AS constituencies_candidates_63_plus,
                TRY_CAST(constituencies_with_candidates_numbering___total_candidates AS BIGINT) AS total_candidates,
                TRY_CAST(candidates_in_a_constituency___min AS BIGINT)               AS candidates_min,
                TRY_CAST(candidates_in_a_constituency___max AS BIGINT)               AS candidates_max,
                TRY_CAST(candidates_in_a_constituency___avg AS DOUBLE)               AS candidates_avg
            FROM "{_CANDIDATES}"
            WHERE state_ut IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_PC_HIGHLIGHTS}-transform",
        deps=[_PC_HIGHLIGHTS],
        sql=f'''
            SELECT
                CAST(state_ut___code AS VARCHAR)          AS state_ut_code,
                CAST(constituency_name___code AS VARCHAR) AS constituency_name_code,
                TRY_CAST(const__no_ AS BIGINT)            AS constituency_no,
                CAST(candidates_ AS VARCHAR)              AS candidates_category,
                TRY_CAST(male AS BIGINT)                  AS male,
                TRY_CAST(female AS BIGINT)                AS female,
                TRY_CAST("_tg_" AS BIGINT)                AS third_gender,
                TRY_CAST("_total" AS BIGINT)              AS total
            FROM "{_PC_HIGHLIGHTS}"
            WHERE constituency_name___code IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id=f"{_SUCCESSFUL}-transform",
        deps=[_SUCCESSFUL],
        sql=f'''
            SELECT
                TRY_CAST("_sl__no_" AS BIGINT)        AS sl_no,
                CAST(state AS VARCHAR)                AS state,
                TRY_CAST(const_no_ AS BIGINT)         AS constituency_no,
                CAST(constituency AS VARCHAR)         AS constituency,
                CAST(constituency_type AS VARCHAR)    AS constituency_type,
                TRY_CAST(total_valid_votes AS BIGINT) AS total_valid_votes,
                CAST(winner_name AS VARCHAR)          AS winner_name,
                CAST(social_category AS VARCHAR)      AS winner_social_category,
                CAST(gender AS VARCHAR)               AS winner_gender,
                CAST(party AS VARCHAR)                AS winner_party,
                CAST(party_symbol AS VARCHAR)         AS winner_party_symbol,
                TRY_CAST(vote_secured AS BIGINT)      AS winner_vote_secured,
                CAST(runner_up_name AS VARCHAR)       AS runner_up_name,
                TRY_CAST(margin AS BIGINT)            AS margin,
                TRY_CAST(margin__ AS DOUBLE)          AS margin_pct
            FROM "{_SUCCESSFUL}"
            WHERE winner_name IS NOT NULL
        ''',
    ),
]
