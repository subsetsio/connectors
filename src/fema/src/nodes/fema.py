"""FEMA / OpenFEMA connector.

OpenFEMA (https://www.fema.gov/about/openfema/api) is a catalog of ~44 public
datasets, each exposed as a per-dataset full-corpus file download at
    https://www.fema.gov/api/open/<version>/<EntityName>.parquet
The server-generated parquet is already cleanly typed (dates -> timestamps,
flags -> bool, ids -> int/str), so the download is a verbatim byte-for-byte
stream of the source parquet into the raw store and the transform is a thin
`SELECT *` that republishes it as a Delta table.

Fetch shape: **stateless full re-pull** (shape 1). Every dataset is a single
stable URL returning the whole corpus; we re-fetch in full each run and
overwrite. No watermark/cursor — revisions and late corrections are picked up
for free. The handful of very large datasets (FimaNfipPolicies ~73.6M rows,
IndividualsAndHouseholdsProgramValidRegistrations ~25.8M, IpawsArchivedAlerts
~4.9M, IndividualAssistanceHousingRegistrantsLargeDisasters ~6.4M, FimaNfipClaims
~2.7M, ...) are streamed chunk-by-chunk straight to the raw store so peak memory
stays bounded regardless of file size. On-demand generation for these can be
slow and occasionally 503s while the server builds the file — both are covered
by the transient-retry decorator.
"""

import httpx
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)
from subsets_utils import NodeSpec, SqlNodeSpec, get_client, raw_writer

# Entity name -> OpenFEMA API version (the path segment v1/v2/v4). Copied from
# the rank-accepted entity union; versions read from the DataSets catalog.
ENTITY_VERSIONS = {
    "DeclarationDenials": 1,
    "DisasterDeclarationsSummaries": 2,
    "EmergencyManagementPerformanceGrants": 2,
    "FemaWebDeclarationAreas": 1,
    "FemaWebDisasterDeclarations": 1,
    "FemaWebDisasterSummaries": 1,
    "FimaNfipClaims": 2,
    "FimaNfipPolicies": 2,
    "HazardMitigationAssistanceMitigatedProperties": 4,
    "HazardMitigationAssistanceProjects": 4,
    "HazardMitigationAssistanceProjectsByNfipCrsCommunities": 2,
    "HazardMitigationAssistanceProjectsFinancialTransactions": 1,
    "HazardMitigationGrantProgramDisasterSummaries": 2,
    "HazardMitigationPlanStatuses": 1,
    "HmaSubapplications": 2,
    "HmaSubapplicationsByNfipCrsCommunities": 1,
    "HmaSubapplicationsCongressionalDistricts": 1,
    "HmaSubapplicationsFinancialTransactions": 1,
    "HmaSubapplicationsProjectSiteInventories": 1,
    "HousingAssistanceOwners": 2,
    "HousingAssistanceRenters": 2,
    "IndividualAssistanceHousingRegistrantsLargeDisasters": 1,
    "IndividualAssistanceMultipleLossFloodProperties": 1,
    "IndividualsAndHouseholdsProgramValidRegistrations": 2,
    "IpawsArchivedAlerts": 1,
    "MissionAssignments": 2,
    "NfipCommunityStatusBook": 1,
    "NfipMultipleLossProperties": 1,
    "NfipResidentialPenetrationRates": 1,
    "NonDisasterAssistanceFirefighterGrants": 1,
    "PublicAssistanceApplicants": 1,
    "PublicAssistanceApplicantsProgramDeliveries": 1,
    "PublicAssistanceFundedProjectsDetails": 2,
    "PublicAssistanceFundedProjectsSummaries": 1,
    "PublicAssistanceGrantAwardActivities": 2,
    "PublicAssistanceSecondAppealsTracker": 1,
    "RegistrationIntakeIndividualsHouseholdPrograms": 2,
    "TrainingClassSchedule": 1,
}

ENTITY_IDS = list(ENTITY_VERSIONS)

# Per-dataset download format. Default is parquet (server-typed, smallest), but
# the OpenFEMA pre-generated full-file does NOT serve parquet for some datasets:
#   - parquet absent from the catalog `distribution` entirely (json-only), or
#   - parquet offered but on-demand full-file generation fails at scale (400 at
#     ~25M rows, 503 at ~73M rows) — confirmed by a full run.
# For those we fall back to a SQL-readable full-file the server DOES serve. This
# is deterministic (one format = one extension per asset) so the transform's
# raw-file glob never sees mixed formats. CSV is read via read_csv_auto and JSONL
# via read_json_auto in the transform.
FORMAT_OVERRIDES = {
    "FimaNfipPolicies": "csv",                              # parquet 503s @73.6M
    "IndividualsAndHouseholdsProgramValidRegistrations": "csv",  # parquet 400 @25.8M
    "PublicAssistanceGrantAwardActivities": "csv",          # parquet not offered
    "IpawsArchivedAlerts": "jsonl",                         # only json formats offered
}

# Datasets whose pre-generated full-file is unreliable: the on-demand generator
# 503s/400s (the origin times out building a multi-GB file and Akamai serves an
# HTML error page, NOT a retryable "still building" response — so plain retry of
# the static URL never converges). The OpenFEMA `$allrecords=true` flag instead
# *streams* the whole corpus directly from the query engine, bypassing the
# file-generation step entirely. Verified 200 + correct content-type for all
# four; the streamed CSV/JSONL carries the same columns (incl. the system `id`)
# as the static file. We scope it to exactly the override datasets — the 34
# parquet datasets serve their cached full-file fine and need no streaming.
ALLRECORDS = set(FORMAT_OVERRIDES)


def _format_for(name: str) -> str:
    return FORMAT_OVERRIDES.get(name, "parquet")


# spec id (f"fema-{name.lower()}") -> (EntityName, version, format). FEMA entity
# names contain no underscores, so the contract's
# f"fema-{eid.lower().replace('_','-')}" reduces to a plain lowercase here.
_BY_SPEC_ID = {
    f"fema-{name.lower().replace('_', '-')}": (name, ver, _format_for(name), name in ALLRECORDS)
    for name, ver in ENTITY_VERSIONS.items()
}

_BASE = "https://www.fema.gov/api/open"

_TRANSIENT_EXC = (
    httpx.ConnectError, httpx.ConnectTimeout, httpx.ReadTimeout,
    httpx.WriteTimeout, httpx.PoolTimeout, httpx.RemoteProtocolError, httpx.ProxyError,
)


class _TransientDownload(Exception):
    """A response that arrived intact at the HTTP layer but is not the dataset:
    an Akamai/Drupal HTML error stub served with a 2xx, or a length-mismatched
    body. Raised so the retry decorator re-fetches instead of writing garbage."""


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, (_TRANSIENT_EXC, _TransientDownload)):
        return True
    if isinstance(exc, httpx.HTTPStatusError):
        code = exc.response.status_code
        # 503 is common while OpenFEMA builds/streams a large corpus on demand;
        # 429 under load. Both clear on a later attempt — they are not permanent.
        return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(8),
    wait=wait_exponential(min=10, max=300),
    reraise=True,
)
def _download(node_id: str, url: str, ext: str, params: dict | None = None) -> None:
    """Stream one full-corpus file verbatim into the raw store under `ext`.

    raise_for_status() fires BEFORE the raw_writer opens, so a permanent 4xx
    leaves no partial file. The whole open-write-stream is inside the retried fn
    so a transient mid-stream failure restarts cleanly (raw_writer overwrites the
    asset under the same extension; the success-path record_write/print only fire
    when the stream completes). Memory is bounded by the chunk size, not the file
    size — required for the multi-GB datasets. We use the shared httpx client's
    streaming interface (a public subsets_utils export) because the buffered
    get() would hold the entire file in RAM.

    Two failure modes peculiar to OpenFEMA-behind-Akamai are folded into the
    transient-retry path rather than being written out as data:
      - a 2xx whose `content-type` is text/html — Akamai's "access denied" /
        Drupal "page not found" stub, served intermittently for the largest
        on-demand corpora instead of the real file;
      - a body shorter than the advertised Content-Length (httpx raises
        RemoteProtocolError itself, but a clean truncation is double-checked).
    Both clear on a later attempt, so we raise `_TransientDownload` to re-fetch.
    The retry budget (8 attempts, backoff to 300s) spans ~15 min — enough to ride
    out the 503/HTML-stub windows the heavy datasets show under concurrent load.
    """
    client = get_client()
    # (connect, read) — read timeout is generous: full-file delivery of the
    # largest datasets streams for minutes.
    with client.stream("GET", url, params=params, timeout=(15.0, 900.0)) as resp:
        resp.raise_for_status()
        ctype = resp.headers.get("content-type", "").lower()
        if "text/html" in ctype:
            # Not the dataset — an Akamai/Drupal error page slipped through as 2xx.
            raise _TransientDownload(f"{node_id}: HTML error stub (content-type={ctype!r})")
        expected = resp.headers.get("content-length")
        written = 0
        with raw_writer(node_id, ext, mode="wb") as out:
            for chunk in resp.iter_bytes(1 << 20):  # 1 MiB
                out.write(chunk)
                written += len(chunk)
        if expected is not None and written != int(expected):
            raise _TransientDownload(
                f"{node_id}: truncated download ({written} of {expected} bytes)"
            )


def fetch_one(node_id: str) -> None:
    """Download one OpenFEMA dataset's full-corpus file. node_id IS the asset
    name; recover the (EntityName, version, format) from it to build the URL."""
    name, version, fmt, allrecords = _BY_SPEC_ID[node_id]
    url = f"{_BASE}/v{version}/{name}.{fmt}"
    # $allrecords streams the whole corpus from the query engine, sidestepping
    # the unreliable on-demand full-file generator for the largest datasets.
    params = {"$allrecords": "true"} if allrecords else None
    _download(node_id, url, fmt, params)


DOWNLOAD_SPECS = [
    NodeSpec(
        id=f"fema-{eid.lower().replace('_', '-')}",
        fn=fetch_one,
        kind="download",
    )
    for eid in ENTITY_IDS
]

# One published Delta table per dataset. The OpenFEMA parquet/csv full files are
# flat tabular, so the transform is a thin pass-through: SELECT * republishes the
# full corpus, and the runtime's 0-rows-is-failure rule guards a broken download.
#
# IpawsArchivedAlerts is the exception: its JSONL carries nested list/struct
# columns (`info`, `code`), a raw CAP-XML `originalMessage`, and geo blobs. A
# SELECT * would publish unusable nested columns, so we project the flat alert
# metadata (one row per alert: who/when/what/scope) and stringify `code`.
_IPAWS = "fema-ipawsarchivedalerts"
_CUSTOM_SQL = {
    _IPAWS: f'''
        SELECT
            id,
            identifier,
            sender,
            TRY_CAST(sent AS TIMESTAMP) AS sent,
            status,
            msgType,
            source,
            scope,
            restriction,
            note,
            cogId,
            xmlns,
            array_to_string(code, ',') AS code
        FROM "{_IPAWS}"
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_CUSTOM_SQL.get(s.id, f'SELECT * FROM "{s.id}"'),
    )
    for s in DOWNLOAD_SPECS
]
