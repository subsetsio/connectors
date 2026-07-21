"""Download specs for the U.S. Senate Lobbying Disclosure Act REST API."""

import pyarrow as pa

from subsets_utils import MaintainSpec, NodeSpec, save_raw_parquet
from utils import (
    API_BASE,
    _auth_headers,
    _crawl_dated,
    _crawl_paged,
    _fetch,
    _name,
    dated_complete,
    reference_complete,
)


def _flat_filing(f: dict) -> list[dict]:
    reg = f.get("registrant") or {}
    cl = f.get("client") or {}
    return [{
        "filing_uuid": f.get("filing_uuid"),
        "filing_year": f.get("filing_year"),
        "filing_type": f.get("filing_type"),
        "filing_type_display": f.get("filing_type_display"),
        "filing_period": f.get("filing_period"),
        "filing_period_display": f.get("filing_period_display"),
        "income": f.get("income"),
        "expenses": f.get("expenses"),
        "dt_posted": f.get("dt_posted"),
        "termination_date": f.get("termination_date"),
        "filing_document_url": f.get("filing_document_url"),
        "registrant_id": reg.get("id"),
        "registrant_name": reg.get("name"),
        "registrant_state": reg.get("state"),
        "registrant_country": reg.get("country"),
        "client_id": cl.get("id"),
        "client_name": cl.get("name"),
        "client_state": cl.get("state"),
        "client_country": cl.get("country"),
    }]


def _explode_activities(f: dict) -> list[dict]:
    reg = f.get("registrant") or {}
    cl = f.get("client") or {}
    out = []
    for activity in f.get("lobbying_activities") or []:
        names = [
            name
            for name in (
                _name(entry.get("lobbyist") or {})
                for entry in activity.get("lobbyists") or []
            )
            if name
        ]
        govs = [
            entity.get("name")
            for entity in activity.get("government_entities") or []
            if entity.get("name")
        ]
        out.append({
            "filing_uuid": f.get("filing_uuid"),
            "filing_year": f.get("filing_year"),
            "dt_posted": f.get("dt_posted"),
            "registrant_name": reg.get("name"),
            "client_name": cl.get("name"),
            "issue_code": activity.get("general_issue_code"),
            "issue_area": activity.get("general_issue_code_display"),
            "description": activity.get("description"),
            "lobbyist_names": names or None,
            "government_entities": govs or None,
        })
    return out


def _flat_contribution(c: dict) -> list[dict]:
    reg = c.get("registrant") or {}
    lob = c.get("lobbyist") or {}
    return [{
        "filing_uuid": c.get("filing_uuid"),
        "filing_year": c.get("filing_year"),
        "filing_type": c.get("filing_type"),
        "filing_type_display": c.get("filing_type_display"),
        "filing_period": c.get("filing_period"),
        "dt_posted": c.get("dt_posted"),
        "filer_type": c.get("filer_type"),
        "filer_type_display": c.get("filer_type_display"),
        "contact_name": c.get("contact_name"),
        "state": c.get("state"),
        "country": c.get("country"),
        "no_contributions": c.get("no_contributions"),
        "registrant_id": reg.get("id"),
        "registrant_name": reg.get("name"),
        "lobbyist_id": lob.get("id"),
        "lobbyist_name": _name(lob),
    }]


def _explode_items(c: dict) -> list[dict]:
    out = []
    for item in c.get("contribution_items") or []:
        out.append({
            "filing_uuid": c.get("filing_uuid"),
            "filing_year": c.get("filing_year"),
            "dt_posted": c.get("dt_posted"),
            "contribution_type": item.get("contribution_type"),
            "contribution_type_display": item.get("contribution_type_display"),
            "contributor_name": item.get("contributor_name"),
            "payee_name": item.get("payee_name"),
            "honoree_name": item.get("honoree_name"),
            "amount": item.get("amount"),
            "contribution_date": item.get("date"),
        })
    return out


def _flat_registrant(r: dict) -> dict:
    return {k: r.get(k) for k in (
        "id", "house_registrant_id", "name", "description", "city", "state",
        "state_display", "country", "country_display", "ppb_country",
        "contact_name", "dt_updated",
    )}


def _flat_client(c: dict) -> dict:
    reg = c.get("registrant") or {}
    data = {k: c.get(k) for k in (
        "id", "client_id", "name", "general_description", "state",
        "state_display", "country", "country_display", "ppb_state",
        "ppb_country", "effective_date", "client_self_select",
    )}
    data["registrant_id"] = reg.get("id")
    data["registrant_name"] = reg.get("name")
    return data


def _flat_lobbyist(lobbyist: dict) -> dict:
    reg = lobbyist.get("registrant") or {}
    data = {k: lobbyist.get(k) for k in (
        "id", "prefix_display", "first_name", "nickname", "middle_name",
        "last_name", "suffix_display",
    )}
    data["registrant_id"] = reg.get("id")
    data["registrant_name"] = reg.get("name")
    return data


def fetch_filings(node_id: str) -> bool | None:
    return _crawl_dated(node_id, "filings", _flat_filing)


def fetch_lobbying_activities(node_id: str) -> bool | None:
    return _crawl_dated(node_id, "filings", _explode_activities)


def fetch_contributions(node_id: str) -> bool | None:
    return _crawl_dated(node_id, "contributions", _flat_contribution)


def fetch_contribution_items(node_id: str) -> bool | None:
    return _crawl_dated(node_id, "contributions", _explode_items)


def fetch_registrants(node_id: str) -> bool | None:
    return _crawl_paged(node_id, "registrants", _flat_registrant)


def fetch_clients(node_id: str) -> bool | None:
    return _crawl_paged(node_id, "clients", _flat_client)


def fetch_lobbyists(node_id: str) -> bool | None:
    return _crawl_paged(node_id, "lobbyists", _flat_lobbyist)


CONSTANT_ENDPOINTS = {
    "senate-lda-filing-types": "constants/filing/filingtypes/",
    "senate-lda-lobbying-issue-codes": "constants/filing/lobbyingactivityissues/",
    "senate-lda-government-entities": "constants/filing/governmententities/",
    "senate-lda-contribution-item-types": "constants/contribution/itemtypes/",
}


CONSTANT_SCHEMAS = {
    "senate-lda-filing-types": pa.schema([
        ("filing_type", pa.string()),
        ("filing_type_display", pa.string()),
    ]),
    "senate-lda-lobbying-issue-codes": pa.schema([
        ("code", pa.string()),
        ("description", pa.string()),
    ]),
    "senate-lda-government-entities": pa.schema([
        ("id", pa.int64()),
        ("name", pa.string()),
    ]),
    "senate-lda-contribution-item-types": pa.schema([
        ("contribution_type", pa.string()),
        ("contribution_type_display", pa.string()),
    ]),
}


def fetch_constant_table(node_id: str) -> None:
    endpoint = CONSTANT_ENDPOINTS[node_id]
    data = _fetch(f"{API_BASE}/{endpoint}", {}, _auth_headers())
    if isinstance(data, dict):
        rows = data.get("results") or []
    else:
        rows = data
    save_raw_parquet(pa.Table.from_pylist(rows, schema=CONSTANT_SCHEMAS[node_id]), node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="senate-lda-filings", fn=fetch_filings, kind="download"),
    NodeSpec(id="senate-lda-lobbying-activities", fn=fetch_lobbying_activities, kind="download"),
    NodeSpec(id="senate-lda-contributions", fn=fetch_contributions, kind="download"),
    NodeSpec(id="senate-lda-contribution-items", fn=fetch_contribution_items, kind="download"),
    NodeSpec(id="senate-lda-registrants", fn=fetch_registrants, kind="download"),
    NodeSpec(id="senate-lda-clients", fn=fetch_clients, kind="download"),
    NodeSpec(id="senate-lda-lobbyists", fn=fetch_lobbyists, kind="download"),
    NodeSpec(id="senate-lda-filing-types", fn=fetch_constant_table, kind="download"),
    NodeSpec(id="senate-lda-lobbying-issue-codes", fn=fetch_constant_table, kind="download"),
    NodeSpec(id="senate-lda-government-entities", fn=fetch_constant_table, kind="download"),
    NodeSpec(id="senate-lda-contribution-item-types", fn=fetch_constant_table, kind="download"),
]


MAINTAIN_SPECS = [
    MaintainSpec(
        asset_id="senate-lda-filings",
        description=(
            "LDA filings are posted continuously per https://lda.senate.gov/api/; "
            "skip only when all monthly fragments exist and the current month is <=7 days old."
        ),
        check=lambda aid: dated_complete(aid, "filings", max_age_days=7),
    ),
    MaintainSpec(
        asset_id="senate-lda-lobbying-activities",
        description=(
            "LDA filing activity rows inherit the continuously posted filings cadence; "
            "skip only when all monthly fragments exist and the current month is <=7 days old."
        ),
        check=lambda aid: dated_complete(aid, "filings", max_age_days=7),
    ),
    MaintainSpec(
        asset_id="senate-lda-contributions",
        description=(
            "LD-203 contribution reports are posted through the LDA API; skip only "
            "when all monthly fragments since 2008 exist and the current month is <=30 days old."
        ),
        check=lambda aid: dated_complete(aid, "contributions", max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-contribution-items",
        description=(
            "LD-203 contribution item rows inherit contribution report posting cadence; "
            "skip only when all monthly fragments since 2008 exist and the current month is <=30 days old."
        ),
        check=lambda aid: dated_complete(aid, "contributions", max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-registrants",
        description=(
            "Registrant directory has no published bulk export or validator; "
            "skip completed raw crawls younger than 30 days."
        ),
        check=lambda aid: reference_complete(aid, max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-clients",
        description=(
            "Client directory has no published bulk export or validator; "
            "skip completed raw crawls younger than 30 days."
        ),
        check=lambda aid: reference_complete(aid, max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-lobbyists",
        description=(
            "Lobbyist directory has no published bulk export or validator; "
            "skip completed raw crawls younger than 30 days."
        ),
        check=lambda aid: reference_complete(aid, max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-filing-types",
        description="LDA filing type constants are small reference data; skip raw assets younger than 30 days.",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-lobbying-issue-codes",
        description="LDA lobbying issue constants are small reference data; skip raw assets younger than 30 days.",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-government-entities",
        description="LDA government entity constants are small reference data; skip raw assets younger than 30 days.",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=30),
    ),
    MaintainSpec(
        asset_id="senate-lda-contribution-item-types",
        description="LDA contribution item type constants are small reference data; skip raw assets younger than 30 days.",
        check=lambda aid: raw_asset_exists(aid, "ndjson.zst", max_age_days=30),
    ),
]
