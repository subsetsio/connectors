"""Inter-Parliamentary Union (IPU Parline) connector.

Source: IPU Parline REST API v3 — https://api.data.ipu.org/v1/ (public, no auth,
JSON:API-style, CC BY-NC-SA 4.0). Each list endpoint returns its full corpus in
one paged request; the DB is updated daily and there is no modified-since cursor,
so every refresh is a stateless full re-pull (corpora are small — the largest is
~4.4k rows). No bulk dump exists; the API list endpoints ARE the bulk path.

Two response shapes are handled:
  * Wrapped JSON:API entities (countries/parliaments/chambers/elections/
    specialized_bodies): each row is {id, type, attributes}, and every attribute
    is itself a wrapper — either {value, missing_reason, annotation} (single) or
    a list of {value, date_from, date_to, ...} (historical). `_unwrap` pulls the
    current value; `_scalar` collapses the bilingual {en,fr} / {term} / {type,value}
    / {from,to} sub-objects to a single scalar. We project a curated set of clean,
    statistically-meaningful fields per entity.
  * Flat entities (political_parties/people) and the precomputed /reports/* tables:
    rows are already flat; only {en,fr}/{term}/{from,to} collapsing is needed.

Raw is saved as NDJSON (drift-safe given the heterogeneous source); the SQL
transforms read it back through DuckDB and do a thin parse/cast pass.
"""

import pyarrow  # noqa: F401  (kept available for parity with other connectors)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    transient_retry,
)

BASE = "https://api.data.ipu.org/v1"
SLUG = "inter-parliamentary-union"
PAGE_SIZE = 5000          # API max; the largest corpus (~4.4k) fits in one page
MAX_PAGES = 50            # safety ceiling — raises on runaway pagination


@transient_retry()
def _get_json(url: str) -> dict:
    resp = get(url, headers={"Accept-Language": "en"}, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _rows_of(payload: dict) -> list:
    data = payload.get("data")
    if isinstance(data, dict):
        return list(data.values())
    if isinstance(data, list):
        return data
    return []


def _fetch_all_list(path: str) -> list:
    """Page a JSON:API list endpoint to completion using meta.total."""
    rows: list = []
    total = None
    page = 1
    while True:
        payload = _get_json(f"{BASE}/{path}/?page[number]={page}&page[size]={PAGE_SIZE}")
        batch = _rows_of(payload)
        rows.extend(batch)
        meta_total = payload.get("meta", {}).get("total")
        if isinstance(meta_total, int):
            total = meta_total
        if total is not None and len(rows) >= total:
            break
        if not batch or len(batch) < PAGE_SIZE:
            break
        page += 1
        if page > MAX_PAGES:
            raise RuntimeError(f"{path}: exceeded MAX_PAGES={MAX_PAGES} (source grew?)")
    return rows


# ── value flattening ───────────────────────────────────────────────────────────

def _scalar(v):
    """Collapse a Parline value object to a single scalar."""
    if isinstance(v, dict):
        if "en" in v:
            return v["en"]
        if "term" in v:
            return v["term"]
        if "value" in v and "type" in v:        # money {type, value}
            return v["value"]
        if "from" in v:                          # date range {from, to}
            return v["from"]
        return None
    if isinstance(v, (str, int, float, bool)) or v is None:
        return v
    return None                                  # lists / nested -> drop


def _unwrap(attr):
    """Pull the current value out of a wrapped JSON:API attribute."""
    if isinstance(attr, list):
        if not attr:
            return None
        current = [e for e in attr if isinstance(e, dict) and not e.get("date_to")]
        entry = current[-1] if current else attr[-1]
        return entry.get("value") if isinstance(entry, dict) else None
    if isinstance(attr, dict):
        return attr.get("value")
    return attr


# ── per-entity curated projections ─────────────────────────────────────────────

# Wrapped JSON:API entities: node-suffix -> (api_path, [attribute keys to project])
WRAPPED = {
    "countries": ("countries", [
        "country_code", "country_name_current", "official_name", "iso_alpha3",
        "iso_numeric3", "region", "subregion", "political_system",
        "population_in_thousands", "members_per_country", "inhabitants_per_parliament",
        "ppp_conversion_factor", "parliament_devoted_budget_perc", "ipu_membership",
        "telephone_calling_code",
    ]),
    "parliaments": ("parliaments", [
        "parliament_code", "parliament_country", "parliament_name",
        "parliament_name_full", "structure_of_parliament", "is_bicameral",
        "date_of_independence", "first_woman_in_parliament_year",
        "first_woman_speaker_year", "compulsory_voting", "num_permanent_staff",
        "num_laws_adopt_parliament_per_year",
    ]),
    "chambers": ("chambers", [
        "chamber_code", "parliament", "chamber_name", "chamber_name_full",
        "struct_parl_status", "designation_mode", "electoral_system",
        "current_members_number", "current_men_number", "current_women_number",
        "current_women_percent", "statutory_members_number", "directly_elected_number",
        "age_average", "total_younger_30_percentage", "total_younger_40_percentage",
        "total_younger_45_percentage", "total_older_46_percentage",
        "female_younger_45_percentage", "gender_quota_or_reserved_seats",
        "youth_quota_or_reserved_seats", "is_electoral_quota_women",
        "min_age_member_parl", "min_age_vote_elect", "basic_salary",
        "num_cham_perm_committees", "groups_number",
        "permanent_staff_number", "parliamentary_term", "num_days_parl_plen",
        "last_election", "num_written_question_ask", "num_written_question_answ",
    ]),
    "elections": ("elections", [
        "election_code", "chamber", "election_date", "election_title",
    ]),
    "specialized-bodies": ("specialized_bodies", [
        "specialized_body_code", "specialized_body_name", "nature",
        "carry_out_inquiries", "hold_oral_evidence_hearing",
        "publishes_reports_on_its_w", "reports_regularly_to_parli",
        "scr_state_compliance",
    ]),
}

# Flat entities: node-suffix -> (api_path, [keys to project])
FLAT = {
    "political-parties": ("political_parties", [
        "political_party_code", "party_name", "political_party_country",
    ]),
    "people": ("people", [
        "person_code", "title_salutation", "first_name", "family_name",
        "gender", "dob_year", "dob_month", "dob_day", "person_country",
    ]),
}

# Precomputed report tables: node-suffix -> report path
REPORTS = {
    "report-women-ranking": "women-ranking",
    "report-age-brackets": "age-brackets",
    "report-speakers": "speakers",
    "report-secretaries-general": "secretaries-general",
    "report-women-speakers": "women-speakers",
    "report-elections": "elections",
}

# Columns dropped from report rows (nested / internal, not SQL-friendly).
_REPORT_DROP = {"_id", "chamber_contact"}


def _suffix(node_id: str) -> str:
    return node_id[len(SLUG) + 1:]


def fetch_one(node_id: str) -> None:
    """Single generic fetch — recovers the entity from the spec id."""
    asset = node_id
    suffix = _suffix(node_id)

    if suffix in WRAPPED:
        api_path, keys = WRAPPED[suffix]
        rows_raw = _fetch_all_list(api_path)
        out = []
        for r in rows_raw:
            attrs = r.get("attributes", {}) if isinstance(r, dict) else {}
            out.append({k: _scalar(_unwrap(attrs.get(k))) for k in keys})
        save_raw_ndjson(out, asset)
        return

    if suffix in FLAT:
        api_path, keys = FLAT[suffix]
        rows_raw = _fetch_all_list(api_path)
        out = [{k: _scalar(r.get(k)) for k in keys} for r in rows_raw if isinstance(r, dict)]
        save_raw_ndjson(out, asset)
        return

    if suffix in REPORTS:
        payload = _get_json(f"{BASE}/reports/{REPORTS[suffix]}")
        rows_raw = _rows_of(payload)
        # union of keys (minus drops) so every row is schema-uniform for DuckDB
        keys = []
        seen = set()
        for r in rows_raw:
            if not isinstance(r, dict):
                continue
            for k in r:
                if k not in seen and k not in _REPORT_DROP:
                    seen.add(k)
                    keys.append(k)
        out = [{k: _scalar(r.get(k)) for k in keys}
               for r in rows_raw if isinstance(r, dict)]
        # Reports are snapshot tables; drop columns that are entirely empty in
        # this snapshot (no information, only noise) while keeping meaningful
        # low-variance columns (e.g. sex='female' in the women-speakers view).
        empty = [k for k in keys if all(r.get(k) in (None, "") for r in out)]
        if empty:
            out = [{k: v for k, v in r.items() if k not in empty} for r in out]
        save_raw_ndjson(out, asset)
        return

    raise ValueError(f"unknown entity suffix: {suffix!r}")


# ── specs ───────────────────────────────────────────────────────────────────────

# Entity union (rank-active). node-suffix per entry; derives the spec id.
ENTITY_SUFFIXES = [
    "chambers", "countries", "elections", "parliaments", "people",
    "political-parties", "report-age-brackets", "report-elections",
    "report-secretaries-general", "report-speakers", "report-women-ranking",
    "report-women-speakers", "specialized-bodies",
]

DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{suffix}", fn=fetch_one, kind="download")
    for suffix in ENTITY_SUFFIXES
]

# Primary-key column per subset (non-null filter in the transform).
_PK = {
    "chambers": "chamber_code",
    "countries": "country_code",
    "elections": "election_code",
    "parliaments": "parliament_code",
    "people": "person_code",
    "political-parties": "political_party_code",
    "specialized-bodies": "specialized_body_code",
    "report-women-ranking": "country_code",
    "report-age-brackets": "chamber_code",
    "report-elections": "chamber_code",
    "report-secretaries-general": "chamber_code",
    "report-speakers": "chamber_code",
    "report-women-speakers": "chamber_code",
}


def _transform_sql(download_id: str, suffix: str) -> str:
    pk = _PK[suffix]
    if suffix == "report-women-ranking":
        # percent fields arrive as strings; cast them to clean doubles.
        return f'''
            SELECT
                * EXCLUDE (lower_chamber_percent_women, upper_chamber_percent_women),
                TRY_CAST(lower_chamber_percent_women AS DOUBLE) AS lower_chamber_percent_women,
                TRY_CAST(upper_chamber_percent_women AS DOUBLE) AS upper_chamber_percent_women
            FROM "{download_id}"
            WHERE "{pk}" IS NOT NULL
        '''
    return f'SELECT * FROM "{download_id}" WHERE "{pk}" IS NOT NULL'


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_transform_sql(s.id, _suffix(s.id)),
    )
    for s in DOWNLOAD_SPECS
]
