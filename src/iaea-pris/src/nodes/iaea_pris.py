"""IAEA PRIS — Power Reactor Information System connector.

PRIS exposes no API, no CSV/JSON/SDMX, and no bulk export — only server-rendered
ASP.NET HTML pages. Per-reactor detail pages live at a stable URL keyed by a
sequential integer id:

    https://pris.iaea.org/pris/CountryStatistics/ReactorDetails.aspx?current=N

Each page is one self-contained HTML doc carrying BOTH the reactor's static
specification block (id-stamped <span> fields) AND its annual operating-history
table (one row per year). We publish two subsets, each its own download node:

  * iaea-pris-reactors      — one row per reactor (specifications)
  * iaea-pris-performance   — one row per (reactor, year) (annual time series)

Both subsets come from the same set of pages; with two independent download
nodes the site is scraped once per node (the harness has no shared-state channel
between download nodes). The corpus is small (~720 reactors), so a full re-scrape
per node is cheap and is the simplest correct shape.

Enumeration: ids are sparse — valid ids run 1..~1124 today with internal gaps up
to ~44 wide, and *unassigned* ids return HTTP 500 (not 404). So we iterate from
1, treat any non-200 as "no such reactor" (a gap), and stop only after a long run
of consecutive misses (comfortably wider than the largest observed gap). New
reactors get appended at the growing edge, so this adapts to growth without a
hardcoded count cap. An absolute id ceiling guards against a runaway loop and
RAISES if hit.

No incremental query parameter exists — full corpus re-scrape each refresh. The
maintain step (authored later) decides whether a node runs on a given refresh;
if a fetch fn is invoked, it fetches.

TLS note: the IAEA host negotiates a cipher that OpenSSL 3's default
SECLEVEL=2 rejects (handshake closes with EOF), while curl/browsers succeed. We
must lower to SECLEVEL=1. subsets_utils.configure_http does not wire a custom
SSL context through to its httpx client, so we install a SECLEVEL=1 client onto
the http_client module once per process; all requests still flow through
subsets_utils.get (logging/tracking preserved).
"""

import re
import ssl
from datetime import datetime

import httpx
import pyarrow as pa

from subsets_utils import get, http_client, save_raw_parquet, transient_retry

BASE_URL = "https://pris.iaea.org/pris/CountryStatistics/ReactorDetails.aspx"
SPAN_PREFIX = "MainContent_MainContent_"

# Enumeration bounds. Largest gap observed between consecutive valid ids is ~44;
# 120 consecutive misses is a safe "we're past the end" signal with headroom for
# growth. HARD_MAX_ID is a runaway safety ceiling — hitting it RAISES.
CONSEC_MISS_STOP = 120
HARD_MAX_ID = 6000

_CLIENT_READY = False


def _ensure_client() -> None:
    """Install a SECLEVEL=1 httpx client onto subsets_utils.http_client.

    The IAEA TLS endpoint requires a cipher rejected by OpenSSL 3's default
    security level. configure_http() cannot pass a custom SSL context, so we set
    the module client directly. Requests still go through subsets_utils.get, so
    request logging/tracking is unaffected. Idempotent per process.
    """
    global _CLIENT_READY
    if _CLIENT_READY:
        return
    ctx = ssl.create_default_context()
    ctx.set_ciphers("DEFAULT@SECLEVEL=1")
    client = httpx.Client(
        timeout=httpx.Timeout(connect=15.0, read=120.0, write=120.0, pool=15.0),
        follow_redirects=True,
        verify=ctx,
        headers={"User-Agent": "subsets.io-connector/1.0 (+https://subsets.io)"},
    )
    if http_client._client is not None:
        try:
            http_client._client.close()
        except Exception:
            pass
    http_client._client = client
    _CLIENT_READY = True


@transient_retry()
def _fetch_page(rid: int) -> httpx.Response:
    """Fetch one reactor page. Returns the response for ANY HTTP status.

    Only genuine transient failures retry: network/transport errors raise out of
    get() (caught by transient_retry), and 429 is re-raised to trigger a retry.
    HTTP 404/500 are NOT retried — for this source they mean "id not assigned"
    (a gap), which the caller treats as a miss. raise_for_status on 5xx would
    turn every gap into a fatal retry storm, so we deliberately do not call it.
    """
    resp = get(BASE_URL, params={"current": rid}, timeout=(15.0, 120.0))
    if resp.status_code == 429:
        resp.raise_for_status()  # transient -> retried by the decorator
    return resp


def _iter_reactor_docs():
    """Yield (reactor_id, lxml_doc) for every valid reactor page, in id order."""
    from lxml import html as lxml_html

    _ensure_client()
    rid = 0
    consecutive_misses = 0
    while True:
        rid += 1
        if rid > HARD_MAX_ID:
            raise RuntimeError(
                f"reactor id scan exceeded HARD_MAX_ID={HARD_MAX_ID} without "
                f"hitting {CONSEC_MISS_STOP} consecutive misses — source layout "
                f"likely changed; refusing to loop unbounded."
            )
        resp = _fetch_page(rid)
        if resp.status_code != 200:
            consecutive_misses += 1
            if consecutive_misses >= CONSEC_MISS_STOP:
                return
            continue
        consecutive_misses = 0
        yield rid, lxml_html.fromstring(resp.text)


# ---------------------------------------------------------------------------
# Parsing helpers
# ---------------------------------------------------------------------------

_UNIT_RE = re.compile(r"\s*(TW\.h|GW\.h|MWe|MWt|MW|h)\s*$")
_YEAR_RE = re.compile(r"\d{4}")


def _span(doc, name: str):
    els = doc.xpath(f"//span[@id='{SPAN_PREFIX}{name}']")
    if not els:
        return None
    txt = " ".join((els[0].text_content() or "").split())
    return txt or None


def _num(s):
    """Parse a numeric field, stripping unit suffixes / %. 'NC', '', non-numeric -> None."""
    if not s:
        return None
    s = s.replace("%", "").replace(",", "").strip()
    s = _UNIT_RE.sub("", s).strip()
    try:
        return float(s)
    except ValueError:
        return None


def _date(s):
    """Parse 'DD Mon, YYYY' (e.g. '25 Oct, 2008') to an ISO date string, else None."""
    if not s:
        return None
    try:
        return datetime.strptime(s, "%d %b, %Y").date().isoformat()
    except ValueError:
        return None


def _country(doc):
    """(country_name, country_code) from the single CountryDetails anchor, or (None, None)."""
    for a in doc.xpath("//a[@href]"):
        m = re.search(r"CountryDetails\.aspx\?current=([A-Za-z]{2})", a.get("href") or "")
        if m:
            name = " ".join((a.text_content() or "").split())
            return (name or None), m.group(1).upper()
    return None, None


def _parse_specs(doc, rid: int) -> dict:
    country, code = _country(doc)
    return {
        "reactor_id": rid,
        "name": _span(doc, "lblReactorName"),
        "alternate_name": _span(doc, "lblAlternateName"),
        "country": country,
        "country_code": code,
        "status": _span(doc, "lblReactorStatus"),
        "reactor_type": _span(doc, "lblType"),
        "model": _span(doc, "lblModel"),
        "reference_unit_power_mwe": _num(_span(doc, "lblNetCapacity")),
        "design_net_capacity_mwe": _num(_span(doc, "lblDesignNetCapacity")),
        "gross_capacity_mwe": _num(_span(doc, "lblGrossCapacity")),
        "thermal_capacity_mwt": _num(_span(doc, "lblThermalCapacity")),
        "construction_start_date": _date(_span(doc, "lblConstructionStartDate")),
        "first_criticality_date": _date(_span(doc, "lblFirstCriticality")),
        "first_grid_connection_date": _date(_span(doc, "lblGridConnectionDate")),
        "commercial_operation_date": _date(_span(doc, "lblCommercialOperationDate")),
        "long_term_shutdown_date": _date(_span(doc, "lblLongTermShutdownDate")),
        "permanent_shutdown_date": _date(_span(doc, "lblPermanentShutdownDate")),
        "lifetime_electricity_supplied_twh": _num(_span(doc, "lblGeneration")),
        "lifetime_operation_factor_pct": _num(_span(doc, "lblOperatingFactor")),
        "lifetime_energy_availability_factor_pct": _num(_span(doc, "lblEAF")),
        "lifetime_load_factor_pct": _num(_span(doc, "lblLoadFactor")),
    }


def _parse_performance(doc, rid: int) -> list:
    """Rows from the annual operating-history table.

    Layout (9 data cells): year, electricity_supplied[GW.h], reference_unit_power[MW],
    annual_time_on_line[h], operation_factor[%], energy_availability_factor annual[%],
    energy_availability_factor cumulative[%], load_factor annual[%], load_factor
    cumulative[%]. We keep the ANNUAL figures (cols 5,7) and drop the running
    cumulative columns. Note/ditto rows ('Data Not Provided', '"') have !=9 cells
    and are skipped.
    """
    rows = []
    for t in doc.xpath("//table"):
        header = [" ".join((c.text_content() or "").split()) for c in t.xpath(".//tr[1]/*")]
        if not header or header[0] != "Year":
            continue
        for tr in t.xpath(".//tr"):
            cells = [" ".join((c.text_content() or "").split()) for c in tr.xpath("./td | ./th")]
            if len(cells) != 9 or not _YEAR_RE.fullmatch(cells[0]):
                continue
            rows.append({
                "reactor_id": rid,
                "year": int(cells[0]),
                "electricity_supplied_gwh": _num(cells[1]),
                "reference_unit_power_mw": _num(cells[2]),
                "annual_time_on_line_h": _num(cells[3]),
                "operation_factor_pct": _num(cells[4]),
                "energy_availability_factor_pct": _num(cells[5]),
                "load_factor_pct": _num(cells[7]),
            })
        break
    return rows


# ---------------------------------------------------------------------------
# Schemas
# ---------------------------------------------------------------------------

REACTORS_SCHEMA = pa.schema([
    ("reactor_id", pa.int64()),
    ("name", pa.string()),
    ("alternate_name", pa.string()),
    ("country", pa.string()),
    ("country_code", pa.string()),
    ("status", pa.string()),
    ("reactor_type", pa.string()),
    ("model", pa.string()),
    ("reference_unit_power_mwe", pa.float64()),
    ("design_net_capacity_mwe", pa.float64()),
    ("gross_capacity_mwe", pa.float64()),
    ("thermal_capacity_mwt", pa.float64()),
    ("construction_start_date", pa.string()),
    ("first_criticality_date", pa.string()),
    ("first_grid_connection_date", pa.string()),
    ("commercial_operation_date", pa.string()),
    ("long_term_shutdown_date", pa.string()),
    ("permanent_shutdown_date", pa.string()),
    ("lifetime_electricity_supplied_twh", pa.float64()),
    ("lifetime_operation_factor_pct", pa.float64()),
    ("lifetime_energy_availability_factor_pct", pa.float64()),
    ("lifetime_load_factor_pct", pa.float64()),
])

PERFORMANCE_SCHEMA = pa.schema([
    ("reactor_id", pa.int64()),
    ("year", pa.int64()),
    ("electricity_supplied_gwh", pa.float64()),
    ("reference_unit_power_mw", pa.float64()),
    ("annual_time_on_line_h", pa.float64()),
    ("operation_factor_pct", pa.float64()),
    ("energy_availability_factor_pct", pa.float64()),
    ("load_factor_pct", pa.float64()),
])


# ---------------------------------------------------------------------------
# Download fns
# ---------------------------------------------------------------------------

def fetch_reactors(node_id: str) -> None:
    rows = [_parse_specs(doc, rid) for rid, doc in _iter_reactor_docs()]
    table = pa.Table.from_pylist(rows, schema=REACTORS_SCHEMA)
    save_raw_parquet(table, node_id)


def fetch_performance(node_id: str) -> None:
    rows = []
    for rid, doc in _iter_reactor_docs():
        rows.extend(_parse_performance(doc, rid))
    table = pa.Table.from_pylist(rows, schema=PERFORMANCE_SCHEMA)
    save_raw_parquet(table, node_id)


# ---------------------------------------------------------------------------
# Specs
# ---------------------------------------------------------------------------

from subsets_utils import NodeSpec, SqlNodeSpec  # noqa: E402

DOWNLOAD_SPECS = [
    NodeSpec(id="iaea-pris-reactors", fn=fetch_reactors, kind="download"),
    NodeSpec(id="iaea-pris-performance", fn=fetch_performance, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="iaea-pris-reactors-transform",
        deps=["iaea-pris-reactors"],
        sql='''
            SELECT
                reactor_id,
                name,
                alternate_name,
                country,
                country_code,
                status,
                reactor_type,
                model,
                reference_unit_power_mwe,
                design_net_capacity_mwe,
                gross_capacity_mwe,
                thermal_capacity_mwt,
                CAST(construction_start_date    AS DATE) AS construction_start_date,
                CAST(first_criticality_date     AS DATE) AS first_criticality_date,
                CAST(first_grid_connection_date AS DATE) AS first_grid_connection_date,
                CAST(commercial_operation_date  AS DATE) AS commercial_operation_date,
                CAST(long_term_shutdown_date    AS DATE) AS long_term_shutdown_date,
                CAST(permanent_shutdown_date    AS DATE) AS permanent_shutdown_date,
                lifetime_electricity_supplied_twh,
                lifetime_operation_factor_pct,
                lifetime_energy_availability_factor_pct,
                lifetime_load_factor_pct
            FROM "iaea-pris-reactors"
            WHERE name IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="iaea-pris-performance-transform",
        deps=["iaea-pris-performance"],
        sql='''
            SELECT
                reactor_id,
                year,
                electricity_supplied_gwh,
                reference_unit_power_mw,
                annual_time_on_line_h,
                operation_factor_pct,
                energy_availability_factor_pct,
                load_factor_pct
            FROM "iaea-pris-performance"
            WHERE electricity_supplied_gwh IS NOT NULL
               OR annual_time_on_line_h IS NOT NULL
               OR load_factor_pct IS NOT NULL
        ''',
    ),
]
