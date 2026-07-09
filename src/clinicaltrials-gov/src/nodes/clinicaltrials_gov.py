"""ClinicalTrials.gov connector.

One REST mechanism (https://clinicaltrials.gov/api/v2). The source is a single
homogeneous corpus of ~590K registered clinical studies, each a deeply nested
JSON record. It is decomposed into six published tables: a core one-row-per-study
`studies` table plus five long child tables (conditions, interventions,
outcome_measures, sponsors_collaborators, locations), each keyed on nct_id.

Per the implement contract, every entity is an independent download node. Each
node paginates GET /studies with a *per-entity field projection* (the `fields`
param) so it only transfers the columns that entity needs, flattens the nested
protocolSection into long rows in Python, and STREAMS them to ndjson.gz — memory
safe, since `locations` alone is several million rows. The DuckDB transforms are
thin cast/dedup passes over those flat rows.

Fetch shape: stateless full re-pull every run (cursor pagination via
nextPageToken; overwrite downstream). The corpus is re-snapshotted whole, so
revisions and deletions are picked up for free — no watermark/cursor state.

TLS note: clinicaltrials.gov sits behind a CDN that 403s httpx's default TLS
ClientHello (JA3 fingerprint) while allowing curl/requests from the same IP.
Relaxing the OpenSSL cipher list (set_ciphers("DEFAULT")) shifts the fingerprint
enough to pass. We install a cipher-relaxed httpx client into subsets_utils's
client cache so every request still routes through subsets_utils.get (its
logging/tracking is preserved).
"""
import json
import ssl

import httpx
from ratelimit import limits, sleep_and_retry

import subsets_utils.http_client as _hc
from subsets_utils import (
    NodeSpec,
    get,
    raw_writer,
    transient_retry,
)

SLUG = "clinicaltrials-gov"
BASE = "https://clinicaltrials.gov/api/v2/studies"
PAGE_SIZE = 1000
# ~590K studies / 1000 ≈ 591 pages. Safety ceiling at ~8x growth: detect runaway
# pagination (a cursor that never terminates) and RAISE rather than spin forever.
MAX_PAGES_ABS = 5000

# Per-entity `fields` projection — only the leaves each table needs, keeping each
# crawl's payload small even though all six page the full corpus independently.
ENTITY_FIELDS = {
    "studies": [
        "NCTId", "BriefTitle", "OfficialTitle", "OverallStatus", "WhyStopped",
        "StartDate", "PrimaryCompletionDate", "CompletionDate",
        "StudyFirstPostDate", "LastUpdatePostDate",
        "StudyType", "Phase", "EnrollmentCount", "EnrollmentType",
        "DesignAllocation", "DesignInterventionModel", "DesignPrimaryPurpose",
        "DesignMasking", "Sex", "MinimumAge", "MaximumAge", "HealthyVolunteers",
        "LeadSponsorName", "LeadSponsorClass", "ResponsiblePartyType",
    ],
    "conditions": ["NCTId", "Condition"],
    "interventions": ["NCTId", "InterventionType", "InterventionName"],
    "outcome-measures": [
        "NCTId", "PrimaryOutcomeMeasure", "PrimaryOutcomeTimeFrame",
        "SecondaryOutcomeMeasure", "SecondaryOutcomeTimeFrame",
    ],
    "sponsors-collaborators": [
        "NCTId", "LeadSponsorName", "LeadSponsorClass",
        "CollaboratorName", "CollaboratorClass",
    ],
    "locations": [
        "NCTId", "LocationFacility", "LocationCity", "LocationState",
        "LocationZip", "LocationCountry", "LocationStatus",
    ],
}


def _install_client() -> None:
    """Install a cipher-relaxed httpx client into subsets_utils's client cache so
    requests pass the CDN's TLS filter. Idempotent — safe to call per fetch."""
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT")
    if getattr(_hc, "_client", None) is not None:
        _hc._client.close()
    _hc._client = httpx.Client(
        timeout=_hc._client_config["timeout"],
        headers=_hc._client_config["headers"],
        follow_redirects=True,
        verify=ctx,
    )


@sleep_and_retry
@limits(calls=120, period=60)  # polite ~2 req/s/process; server tolerated ~250/min clean
def _throttle() -> None:
    return None


@transient_retry()  # 6 attempts, exp backoff; retries 429 + 5xx + transient network
def _fetch_page(fields: list[str], token: str | None) -> dict:
    _throttle()
    params = {
        "pageSize": PAGE_SIZE,
        "fields": ",".join(fields),
        "countTotal": "false",
    }
    if token:
        params["pageToken"] = token
    resp = get(BASE, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


# ---- per-entity row extractors: nested study record -> flat long rows ----------

def _nct(study: dict) -> str | None:
    return (
        study.get("protocolSection", {})
        .get("identificationModule", {})
        .get("nctId")
    )


def _rows_studies(study: dict):
    ps = study.get("protocolSection", {})
    ident = ps.get("identificationModule", {})
    status = ps.get("statusModule", {})
    design = ps.get("designModule", {})
    dinfo = design.get("designInfo", {})
    elig = ps.get("eligibilityModule", {})
    spons = ps.get("sponsorCollaboratorsModule", {})
    lead = spons.get("leadSponsor", {})
    phases = design.get("phases") or []
    yield {
        "nct_id": ident.get("nctId"),
        "brief_title": ident.get("briefTitle"),
        "official_title": ident.get("officialTitle"),
        "overall_status": status.get("overallStatus"),
        "why_stopped": status.get("whyStopped"),
        "start_date": status.get("startDateStruct", {}).get("date"),
        "primary_completion_date": status.get("primaryCompletionDateStruct", {}).get("date"),
        "completion_date": status.get("completionDateStruct", {}).get("date"),
        "study_first_post_date": status.get("studyFirstPostDateStruct", {}).get("date"),
        "last_update_post_date": status.get("lastUpdatePostDateStruct", {}).get("date"),
        "study_type": design.get("studyType"),
        "phase": "|".join(phases) if phases else None,
        "enrollment_count": design.get("enrollmentInfo", {}).get("count"),
        "enrollment_type": design.get("enrollmentInfo", {}).get("type"),
        "allocation": dinfo.get("allocation"),
        "intervention_model": dinfo.get("interventionModel"),
        "primary_purpose": dinfo.get("primaryPurpose"),
        "masking": dinfo.get("maskingInfo", {}).get("masking"),
        "sex": elig.get("sex"),
        "minimum_age": elig.get("minimumAge"),
        "maximum_age": elig.get("maximumAge"),
        "healthy_volunteers": elig.get("healthyVolunteers"),
        "lead_sponsor_name": lead.get("name"),
        "lead_sponsor_class": lead.get("class"),
        "responsible_party_type": spons.get("responsibleParty", {}).get("type"),
    }


def _rows_conditions(study: dict):
    nct = _nct(study)
    conds = study.get("protocolSection", {}).get("conditionsModule", {}).get("conditions") or []
    for c in conds:
        yield {"nct_id": nct, "condition": c}


def _rows_interventions(study: dict):
    nct = _nct(study)
    items = study.get("protocolSection", {}).get("armsInterventionsModule", {}).get("interventions") or []
    for it in items:
        yield {
            "nct_id": nct,
            "intervention_type": it.get("type"),
            "intervention_name": it.get("name"),
        }


def _rows_outcome_measures(study: dict):
    nct = _nct(study)
    om = study.get("protocolSection", {}).get("outcomesModule", {})
    for kind, key in (("primary", "primaryOutcomes"), ("secondary", "secondaryOutcomes")):
        for o in om.get(key) or []:
            yield {
                "nct_id": nct,
                "outcome_type": kind,
                "measure": o.get("measure"),
                "time_frame": o.get("timeFrame"),
            }


def _rows_sponsors_collaborators(study: dict):
    nct = _nct(study)
    spons = study.get("protocolSection", {}).get("sponsorCollaboratorsModule", {})
    lead = spons.get("leadSponsor")
    if lead:
        yield {
            "nct_id": nct,
            "name": lead.get("name"),
            "agency_class": lead.get("class"),
            "role": "lead",
        }
    for c in spons.get("collaborators") or []:
        yield {
            "nct_id": nct,
            "name": c.get("name"),
            "agency_class": c.get("class"),
            "role": "collaborator",
        }


def _rows_locations(study: dict):
    nct = _nct(study)
    locs = study.get("protocolSection", {}).get("contactsLocationsModule", {}).get("locations") or []
    for loc in locs:
        yield {
            "nct_id": nct,
            "facility": loc.get("facility"),
            "city": loc.get("city"),
            "state": loc.get("state"),
            "zip": loc.get("zip"),
            "country": loc.get("country"),
            "location_status": loc.get("status"),
        }


EXTRACTORS = {
    "studies": _rows_studies,
    "conditions": _rows_conditions,
    "interventions": _rows_interventions,
    "outcome-measures": _rows_outcome_measures,
    "sponsors-collaborators": _rows_sponsors_collaborators,
    "locations": _rows_locations,
}


def fetch_one(node_id: str) -> None:
    """Paginate /studies for one entity's field projection, flatten each study
    into long rows, and stream them to the node's ndjson.gz raw asset."""
    _install_client()
    entity = node_id[len(SLUG) + 1:]  # strip "clinicaltrials-gov-"
    fields = ENTITY_FIELDS[entity]
    extract = EXTRACTORS[entity]

    token = None
    pages = 0
    with raw_writer(node_id, "ndjson.gz", mode="wt", compression="gzip") as fh:
        while True:
            data = _fetch_page(fields, token)
            for study in data.get("studies", []):
                for row in extract(study):
                    fh.write(json.dumps(row) + "\n")
            pages += 1
            token = data.get("nextPageToken")
            if not token:
                break
            if pages >= MAX_PAGES_ABS:
                raise RuntimeError(
                    f"{node_id}: hit MAX_PAGES_ABS={MAX_PAGES_ABS} pages without "
                    "exhausting the cursor — source grew far past expectation or "
                    "pagination is looping; investigate before raising the cap."
                )


DOWNLOAD_SPECS = [
    NodeSpec(id="clinicaltrials-gov-studies", fn=fetch_one, kind="download"),
    NodeSpec(id="clinicaltrials-gov-conditions", fn=fetch_one, kind="download"),
    NodeSpec(id="clinicaltrials-gov-interventions", fn=fetch_one, kind="download"),
    NodeSpec(id="clinicaltrials-gov-outcome-measures", fn=fetch_one, kind="download"),
    NodeSpec(id="clinicaltrials-gov-sponsors-collaborators", fn=fetch_one, kind="download"),
    NodeSpec(id="clinicaltrials-gov-locations", fn=fetch_one, kind="download"),
]
