"""Energy Institute - Statistical Review of World Energy connector.

Source: the single consolidated "panel format" CSV published once a year (late
June) by the Energy Institute - the entire Statistical Review of World Energy in
one flat table (~3.8MB; 141 countries/regions x years 1965->latest x ~90 energy
measures in a wide layout: oil/gas/coal/nuclear/hydro/renewables consumption &
production, electricity generation, refining, critical minerals, and emissions).

One request gets the whole corpus, so this is a stateless full re-pull every run
(shape 1): no watermark, no cursor. Revisions and late corrections are picked up
for free because nothing is cached across runs.

URL stability: the numeric asset id in the entry URL
(/file/0011/1659656/panel.csv) is edition-specific and changes with each yearly
release. The current panel.csv link is NOT present in the static HTML of the
downloads page (it is injected client-side), so it cannot be auto-discovered
without a headless browser. The pinned URL below must therefore be refreshed
annually when a new edition ships (~late June).

HTTP layer: the whole energyinst.org site sits behind Cloudflare bot-management
that 403s the CI runner's datacenter IP ("Just a moment..." challenge HTML)
regardless of User-Agent or cookie priming - it fingerprints the TLS/HTTP2
handshake, and httpx (what subsets_utils.get uses) presents a non-browser
fingerprint. We therefore deliberately bypass subsets_utils.get here and use
curl_cffi with Chrome impersonation, which presents Chrome's real TLS/JA3 +
HTTP2 fingerprint and is served normally - the same mechanism the obr/rbnz
connectors use for the same reason. We first GET the human downloads page in the
session (research verified this navigate-then-download clears the gate and seeds
the __cf_bm/_cfuvid cookies), then fetch the asset on the shared cookie jar.
Everything else (raw I/O, etc.) still goes through subsets_utils.

Raw is saved as wide parquet (one row per country-year, ~90 measure columns, a
faithful mirror of the source layout); the transform UNPIVOTs it to the long
format the subset publishes: (country, year, iso3, region, subregion,
measure_code, value).
"""
import io

import pandas as pd
import pyarrow as pa
from curl_cffi import requests as cffi_requests
from curl_cffi.requests.exceptions import (
    ConnectionError as CffiConnectionError,
    HTTPError as CffiHTTPError,
    Timeout as CffiTimeout,
)
from tenacity import retry, retry_if_exception, stop_after_attempt, wait_exponential

from subsets_utils import NodeSpec, save_raw_parquet

# Pinned to the 2025 (74th) edition. Refresh annually - see module docstring.
PANEL_CSV_URL = "https://www.energyinst.org/__data/assets/file/0011/1659656/panel.csv"
# Human downloads page - GET it first to clear the Cloudflare gate and seed cookies.
DOWNLOADS_PAGE = "https://www.energyinst.org/statistical-review/resources-and-data-downloads"

_IMPERSONATE = "chrome"

# String identifier/classification columns. Everything else in the panel that is
# not a classification column (see the transform's EXCLUDE list) is a numeric
# energy measure typed float64.
_STR_DIM_COLS = ("Country", "ISO3166_alpha3", "Region", "SubRegion")

_TRANSIENT_EXC = (CffiConnectionError, CffiTimeout)


class _CloudflareChallenge(Exception):
    """The asset endpoint returned a Cloudflare anti-bot challenge (or any other
    non-CSV payload) instead of the panel CSV. Transient - retried with backoff
    because the managed-challenge gate can clear on a subsequent attempt."""


def _is_transient(exc: BaseException) -> bool:
    if isinstance(exc, _CloudflareChallenge) or isinstance(exc, _TRANSIENT_EXC):
        return True
    if isinstance(exc, CffiHTTPError):
        resp = getattr(exc, "response", None)
        code = getattr(resp, "status_code", None)
        if code is not None:
            return code == 429 or 500 <= code < 600
    return False


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(10),
    wait=wait_exponential(min=4, max=120),
    reraise=True,
)
def _fetch_panel_csv(session) -> bytes:
    # Navigate-then-download: prime the gate/cookies on the human page, then pull
    # the asset on the shared session. The priming GET is best-effort - if it is
    # itself challenged the asset GET below still classifies and retries.
    session.get(DOWNLOADS_PAGE, timeout=120)
    resp = session.get(PANEL_CSV_URL, timeout=180)
    if resp.status_code == 429 or resp.status_code >= 500:
        resp.raise_for_status()  # genuine transient server error -> retried
    body = resp.content
    # The real file is UTF-8-BOM CSV beginning with the "Country,Year" header.
    if resp.status_code == 200 and body[:40].lstrip(b"\xef\xbb\xbf").startswith(b"Country,Year"):
        return body
    raise _CloudflareChallenge(
        f"panel.csv returned a non-CSV payload (status={resp.status_code}, "
        f"{len(body)} bytes): {body[:80]!r}"
    )


def _panel_schema(columns) -> pa.Schema:
    """Wide-table schema built from the live header: Year as int32, the string
    identifier columns as string, every other column (ISO3166_numeric, the
    OPEC/EU/OECD/CIS membership flags, pop, and all energy measures) as a
    nullable float64. Building from the header means a new edition that
    adds/removes measure columns still types cleanly."""
    fields = []
    for col in columns:
        if col == "Year":
            fields.append((col, pa.int32()))
        elif col in _STR_DIM_COLS:
            fields.append((col, pa.string()))
        else:
            fields.append((col, pa.float64()))
    return pa.schema(fields)


def fetch_values(node_id: str) -> None:
    asset = node_id  # the runtime passes the spec id; it IS the asset name
    session = cffi_requests.Session(impersonate=_IMPERSONATE)
    try:
        raw = _fetch_panel_csv(session)
    finally:
        session.close()
    # encoding="utf-8-sig" strips the UTF-8 BOM on the "Country" header.
    df = pd.read_csv(io.BytesIO(raw), encoding="utf-8-sig")
    table = pa.Table.from_pandas(
        df, schema=_panel_schema(df.columns), preserve_index=False
    )
    save_raw_parquet(table, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id="energy-institute-values", fn=fetch_values, kind="download"),
]

# Transforms live as a file pair in src/transforms/energy-institute-values.{sql,yml}
# (the authoring format), not as a module-level TRANSFORM_SPECS list.
