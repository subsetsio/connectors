"""MoSPI (eSankhyiki / NSO India) connector.

Source: the official public REST API at https://api.mospi.gov.in/. Each of the
23 published datasets is one statistical product (CPI, GDP/NAS, PLFS labour
force, ASI industries, NSS rounds, ...). The API is keyed off *indicators*: most
survey datasets require an `indicator_code` (or a survey/frequency/base-year
qualifier) on the data endpoint, so the whole-table pull for a dataset is the
union over its indicator/qualifier cross-product — we enumerate those from the
dataset's own list endpoint, then page the data endpoint for each combo. Index
datasets (CPI, WPI, IIP, CPIALRL) return the full flat table per base-year/series
without an indicator filter.

Fetch shape: stateless full re-pull (shape 1). The API exposes no
since/cursor/modified filter (verified in research), so every refresh pulls the
whole corpus and overwrites. Volumes are low-millions of rows per dataset at
most; we page at 50k/request and stream each page straight to gzipped NDJSON so
no dataset is ever fully held in memory.

Raw format: Parquet, written against an explicit all-string schema (the union of
the sanitized keys across the dataset's combos). Across datasets the columns
differ wildly, and a few carry awkward names (`state/UT`,
`Land_Possessed(hectares)`), so keys are sanitized to `[A-Za-z0-9_]` and scalar
values stringified on write; the transform casts the measure column(s) back to
DOUBLE.

The schema is declared rather than inferred because these are long-format
indicator tables: a dimension column is null for every row of an indicator that
isn't disaggregated along it. Under NDJSON, DuckDB's `read_json_auto` infers
types from a 20480-row sample, so any dimension that happens to be null across
that prefix — 181 columns over the 23 datasets, e.g. `hces.cereal`,
`cpi-getitemindex.inflation` — was typed JSON and published as JSON, and the
type flipped with row order between runs. Parquet carries the schema, so the
column types are exact and stable.

TLS: api.mospi.gov.in serves a valid eMudhra certificate but ships a messy chain
— two distinct intermediates share the subject `EM DV TLS CA - G2A-1`, one
cross-signed by the Comodo `AAA Certificate Services` root (which certifi and
Ubuntu's CA store no longer carry) and one issued by `emSign Root TLS CA - G1`.
OpenSSL's path builder matches the first intermediate by subject, picks the AAA
one, and dead-ends on an untrusted self-signed root. We add both eMudhra
intermediates (`mospi_ca_bundle.pem`) as extra anchors on top of certifi so the
path builder can disambiguate; the chain still terminates at `emSign Root CA -
G1`, which certifi trusts. Verification is never disabled and no distrusted root
is trusted. If eMudhra rotates the intermediate this fails closed with a TLS
error — refresh the bundle (instructions are in its header).

Known limitation: CPI base_year 2024 (the newest rebasing, 2025+ data only) is
served by an undocumented `getCPIData` endpoint that returns 400 for every
parameter combination probed; we cover base_year 2010 and 2012, which carry the
full CPI series through the latest month on the 2012 base. Economic Census (a
one-off 2013-14 census reachable only via dashboard HTML-scraping, not this REST
API) was scored below the publish threshold and is intentionally not built.
"""

import json
import re
from pathlib import Path

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    raw_parquet_writer,
    transient_retry,
)

BASE = "https://api.mospi.gov.in"
PAGE = 50000              # server honours large page sizes; minimises round-trips
ROW_GROUP = 50000         # rows buffered per Parquet row group
MAX_PAGES_ABS = 100000    # safety ceiling — raises (never silently truncates)

# ---------------------------------------------------------------------------
# Transport: route through subsets_utils.get, but back its client with an SSL
# context that can verify the MoSPI chain (see module docstring). subsets_utils
# exposes no supported hook for the client's SSL context, so we swap the private
# module-level client — requests still flow through subsets_utils.get, keeping
# its retry and http_requests.csv tracking.
# ---------------------------------------------------------------------------
CA_BUNDLE = Path(__file__).with_name("mospi_ca_bundle.pem")

_CLIENT_READY = False


def _ensure_client() -> None:
    global _CLIENT_READY
    if _CLIENT_READY:
        return
    import ssl

    import certifi

    from subsets_utils import http_client

    ctx = ssl.create_default_context(cafile=certifi.where())
    ctx.load_verify_locations(cafile=str(CA_BUNDLE))
    client = httpx.Client(
        timeout=httpx.Timeout(180.0, connect=15.0),
        headers={"User-Agent": "subsets.io-data-connector/1.0 (mospi)"},
        follow_redirects=True,
        verify=ctx,
    )
    if http_client._client is not None:
        try:
            http_client._client.close()
        except Exception:
            pass
    http_client._client = client
    _CLIENT_READY = True


# Retries are deliberately short: many invalid (indicator x frequency x ...)
# cross-product combos return a *deterministic* 500, so we want to give up
# quickly and skip the combo rather than burn minutes backing off per dead combo.
# Genuinely transient 5xx/429 still get a few fast retries.
@transient_retry(attempts=4, min_wait=2, max_wait=30)
def _get_json(path: str, params: dict) -> dict:
    _ensure_client()
    resp = get(f"{BASE}{path}", params=params, timeout=(15.0, 180.0))
    resp.raise_for_status()
    text = resp.text
    # Unknown /api/<dataset>/<path> falls through to the Swagger-UI HTML page
    # (HTTP 200) instead of 404 — treat that as a hard bug, not a data row.
    if text.lstrip()[:1] == "<":
        raise ValueError(f"non-JSON (HTML) response from {path} — bad endpoint/params")
    return json.loads(text)


def _get_json_safe(path: str, params: dict):
    """Like _get_json but returns None on a (post-retry) HTTP error or HTML
    fallthrough — used so one dead combo doesn't sink the whole dataset."""
    try:
        return _get_json(path, params)
    except (httpx.HTTPStatusError, ValueError) as e:
        print(f"[mospi] skip {path} {params}: {type(e).__name__}: {str(e)[:120]}")
        return None


def _paginate(path: str, params: dict):
    """Yield every data row across all pages for one query combo."""
    page = 1
    while True:
        p = dict(params)
        p["limit"] = PAGE
        p["page"] = page
        obj = _get_json(path, p)
        data = obj.get("data") if isinstance(obj, dict) else None
        if not data:
            return
        for row in data:
            yield row
        meta = obj.get("meta_data") or {}
        total_pages = meta.get("totalPages")
        if total_pages is not None:
            if page >= int(total_pages):
                return
        elif len(data) < PAGE:
            return
        page += 1
        if page > MAX_PAGES_ABS:
            raise RuntimeError(
                f"{path}: exceeded {MAX_PAGES_ABS} pages for {params} — "
                "source grew past expectations or pagination is looping"
            )


# ---------------------------------------------------------------------------
# Combo builders — enumerate the (indicator / survey / base-year ...) tuples
# that must be queried to cover a dataset's whole table.
# ---------------------------------------------------------------------------
_FMT = {"Format": "JSON"}


def _list(path: str, params: dict | None = None):
    obj = _get_json(path, params or {})
    return obj.get("data", obj) if isinstance(obj, dict) else obj


def _as_items(data, prefer=("indicator", "indicators")):
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        for k in prefer:
            if isinstance(data.get(k), list):
                return data[k]
        for v in data.values():
            if isinstance(v, list):
                return v
    return []


def _codes(items, field):
    out = []
    for it in items:
        if isinstance(it, dict) and it.get(field) is not None:
            out.append(it[field])
    return out


def _simple(list_path, code_field, data_param):
    """[{data_param: code, Format: JSON}, ...] from a flat indicator list."""
    items = _as_items(_list(list_path))
    return [{data_param: c, **_FMT} for c in _codes(items, code_field)]


def _by_frequency(list_path, freqs):
    out = []
    for fc in freqs:
        items = _as_items(_list(list_path, {"frequency_code": fc}))
        for c in _codes(items, "indicator_code"):
            out.append({"indicator_code": c, "frequency_code": fc, **_FMT})
    return out


def _by_survey(list_path, surveys):
    out = []
    for sc in surveys:
        items = _as_items(_list(list_path, {"survey_code": sc}))
        for c in _codes(items, "indicator_code"):
            out.append({"indicator_code": c, "survey_code": sc, **_FMT})
    return out


def _c_energy():
    d = _list("/api/energy/getEnergyIndicatorList")
    inds = _codes(d.get("indicator", []) if isinstance(d, dict) else [], "indicator_code")
    ubs = _codes(d.get("use_of_energy_balance", []) if isinstance(d, dict) else [],
                 "use_of_energy_balance_code")
    return [{"indicator_code": i, "use_of_energy_balance_code": u, **_FMT}
            for i in inds for u in ubs]


def _c_mnre():
    items = _as_items(_list("/api/mnre/getTypeOfRenewableEnergy"))
    return [{"type_of_renewable_energy_code": c, **_FMT}
            for c in _codes(items, "type_of_renewable_energy_code")]


def _c_nss78():
    # list shape: {"indicator": [{"code": 2, "name": ...}]}; data param is the
    # lowercase indicator_code (swagger's "Indicator" 500s).
    items = _as_items(_list("/api/nss-78/getIndicatorList"))
    return [{"indicator_code": c, **_FMT} for c in _codes(items, "code")]


def _c_nas():
    d = _list("/api/nas/getNasIndicatorList")
    bys = _codes(d.get("base_year", []) if isinstance(d, dict) else [], "base_year")
    sers = _codes(d.get("series", []) if isinstance(d, dict) else [], "series")
    fcs = _codes(d.get("frequency", []) if isinstance(d, dict) else [], "frequency_code")
    inds = _codes(d.get("indicator", []) if isinstance(d, dict) else [], "indicator_code")
    qinds = _codes(d.get("quarter_indicator", []) if isinstance(d, dict) else [], "indicator_code")
    out = []
    for by in bys:
        for ser in sers:
            for fc in fcs:
                ind_set = inds if fc == 1 else (qinds or inds)
                for ind in ind_set:
                    out.append({"base_year": by, "series": ser,
                                "frequency_code": fc, "indicator_code": ind, **_FMT})
    return out


def _c_asi():
    items = _as_items(_list("/api/asi/getNicClassificationYear"))
    return [{"classification_year": c, **_FMT}
            for c in _codes(items, "classification_year")]


def _c_cpi():
    d = _list("/api/cpi/getCpiBaseYear")
    bys = [b for b in _codes(d.get("base_year", []) if isinstance(d, dict) else [], "base_year")
           if str(b) != "2024"]  # 2024 served only by undocumented endpoint (see docstring)
    sers = _codes(d.get("series", []) if isinstance(d, dict) else [], "series")
    return [{"base_year": str(by), "series": s, **_FMT} for by in bys for s in sers]


def _c_iip():
    d = _list("/api/iip/getIipBaseYear")
    bys = _codes(d.get("base_year", []) if isinstance(d, dict) else [], "base_year")
    freqs = _codes(d.get("frequency", []) if isinstance(d, dict) else [], "frequency")
    return [{"base_year": by, "frequency": fr, "type": "All", **_FMT}
            for by in bys for fr in freqs]


def _c_wpi():
    items = _as_items(_list("/api/wpi/getWpiBaseYear"))
    return [{"base_year": by, **_FMT} for by in _codes(items, "label")]


# entity_id -> (data endpoint path, combo-builder callable). The builder runs
# inside the fetch subprocess, so live API drift in indicator lists is picked up
# automatically. spec id is f"mospi-{entity_id}".
PLAN = {
    "aishe-getaisherecords":     ("/api/aishe/getAisheRecords",
                                  lambda: _simple("/api/aishe/getAisheIndicatorList", "indicator_code", "indicator_code")),
    "nfhs-getnfhsrecords":       ("/api/nfhs/getNfhsRecords",
                                  lambda: _simple("/api/nfhs/getNfhsIndicatorList", "indicator_code", "indicator_code")),
    "gender-getgenderrecords":   ("/api/gender/getGenderRecords",
                                  lambda: _simple("/api/gender/getGenderIndicatorList", "indicator_code", "indicator_code")),
    "envstats-getenvstatsrecords": ("/api/env/getEnvStatsRecords",
                                  lambda: _simple("/api/env/getEnvStatsIndicatorList", "indicator_code", "indicator_code")),
    "hces-gethcesrecords":       ("/api/hces/getHcesRecords",
                                  lambda: _simple("/api/hces/getHcesIndicatorList", "indicator_code", "indicator_code")),
    "tus-gettusrecords":         ("/api/tus/getTusRecords",
                                  lambda: _simple("/api/tus/getTusIndicatorList", "indicator_code", "indicator_code")),
    "cpialrl-getcpialrlrecords": ("/api/cpialrl/getCpialrlRecords",
                                  lambda: _simple("/api/cpialrl/getCpialrlIndicatorList", "indicator_code", "indicator_code")),
    "udise-getudiserecords":     ("/api/udise/getUdiseRecords",
                                  lambda: _simple("/api/udise/getIndicatorList", "indicator_code", "indicator_code")),
    "nss77-getnss77records":     ("/api/nss-77/getNss77Records",
                                  lambda: _simple("/api/nss-77/getIndicatorList", "indicator_code", "indicator_code")),
    "rbi-getrbirecords":         ("/api/rbi/getRbiRecords",
                                  lambda: _simple("/api/rbi/getRbiIndicatorList", "indicator_code", "sub_indicator_code")),
    "nss78-getnss78records":     ("/api/nss-78/getNss78Records", _c_nss78),
    "asuse-getasuserecords":     ("/api/asuse/getAsuseRecords",
                                  lambda: _by_frequency("/api/asuse/getAsuseIndicatorListByFrequency", (1, 2))),
    "plfs-getdata":              ("/api/plfs/getData",
                                  lambda: _by_frequency("/api/plfs/getIndicatorListByFrequency", (1, 2, 3))),
    "nss76-getnss76records":     ("/api/nss-76/getNss76Records",
                                  lambda: _by_survey("/api/nss-76/getIndicatorList", (1, 2))),
    "nss80-getnss80records":     ("/api/nss-80/getNSS80Records",
                                  lambda: _by_survey("/api/nss-80/getIndicatorList", (1, 2))),
    "energy-getenergyrecords":   ("/api/energy/getEnergyRecords", _c_energy),
    "mnre-getdatabyenergy":      ("/api/mnre/getDataByEnergy", _c_mnre),
    "nas-getnasdata":            ("/api/nas/getNASData", _c_nas),
    "asi-getasidata":            ("/api/asi/getASIData", _c_asi),
    "cpi-getcpiindex":           ("/api/cpi/getCPIIndex", _c_cpi),
    "cpi-getitemindex":          ("/api/cpi/getItemIndex", _c_cpi),
    "iip-getiipdata":            ("/api/iip/getIipData", _c_iip),
    "wpi-getwpirecords":         ("/api/wpi/getWpiRecords", _c_wpi),
}

_KEY_RE = re.compile(r"[^0-9A-Za-z_]")


def _clean_row(row: dict) -> dict:
    out = {}
    for k, v in row.items():
        key = _KEY_RE.sub("_", str(k))
        out[key] = None if v is None else str(v)
    return out


def _combo_keys(data_path: str, combo: dict) -> list[str]:
    """One cheap limit=1 probe to learn a combo's (sanitized) column set.
    Returns [] for a dead/empty combo."""
    p = dict(combo)
    p["limit"] = 1
    p["page"] = 1
    obj = _get_json_safe(data_path, p)
    data = obj.get("data") if isinstance(obj, dict) else None
    if data:
        return list(_clean_row(data[0]).keys())
    return []


def fetch_one(node_id: str) -> None:
    entity = node_id[len("mospi-"):]
    data_path, build_combos = PLAN[entity]
    combos = build_combos()
    if not combos:
        raise RuntimeError(f"{node_id}: combo enumeration returned nothing — list endpoint changed")

    # Pre-pass: the union of column names across every combo. Different combos
    # (base years, indicators, survey modules) return different key sets; one
    # limit=1 probe each yields the dataset's full column set, which becomes the
    # Parquet schema. Every row is then written against it (missing keys ->
    # explicit null), so the file has a single, declared schema.
    keys: list[str] = []
    seen: set[str] = set()
    for combo in combos:
        for k in _combo_keys(data_path, combo):
            if k not in seen:
                seen.add(k)
                keys.append(k)
    if not keys:
        raise RuntimeError(f"{node_id}: no columns discovered across {len(combos)} combos — dataset shape changed")

    schema = pa.schema([(k, pa.string()) for k in keys])
    total = 0
    with raw_parquet_writer(node_id, schema) as w:
        buf: list[dict] = []

        def flush() -> None:
            if buf:
                w.write_batch(pa.RecordBatch.from_pylist(buf, schema=schema))
                buf.clear()

        for combo in combos:
            try:
                for row in _paginate(data_path, combo):
                    cr = _clean_row(row)
                    buf.append({k: cr.get(k) for k in keys})
                    total += 1
                    if len(buf) >= ROW_GROUP:
                        flush()
            except (httpx.HTTPStatusError, ValueError) as e:
                # One dead combo (deterministic 5xx / HTML) — skip, keep the rest.
                print(f"[mospi] skip combo {combo}: {type(e).__name__}: {str(e)[:120]}")
                continue
        flush()

    if total == 0:
        raise RuntimeError(f"{node_id}: 0 rows across {len(combos)} combos — dataset shape changed")


DOWNLOAD_SPECS = [
    NodeSpec(id=f"mospi-{eid}", fn=fetch_one, kind="download")
    for eid in PLAN
]
