"""wmo-values — long-format hydrological observations.

(provider, station, variable, timestamp -> value). Stations are discovered from
the GEO-DAB timeseries-api metadata endpoint; the actual data points come from
**CUAHSI WaterOneFlow** GetSiteInfo (the GetValues-compatible variable codes) +
GetValues (WaterML 1.1). The timeseries-api data path (includeData=true) and its
monitoring-points endpoint both return slow/500 serialization errors, so
WaterOneFlow is the reliable data path (the mechanism research chose).

SCOPE / why this is a bounded snapshot:
WHOS federates ~133 data providers (national hydrological services); big
providers expose thousands of stations each, and the broker is slow (seconds per
GetValues), so a full snapshot of the whole corpus is infeasible in one run.
Crucially, each cloud run writes raw to its OWN run-scoped location
(<connector>/runs/<run_id>/raw) and the transform overwrites the published table
from that run's raw alone — so cross-run "resume and accumulate" does not work
here. The connector is therefore **stateless**: every run re-fetches the same
deterministic scope and overwrites.

To keep that scope broad (many countries) rather than deep (all of one), the
value fetch takes only the first STATIONS_PER_PROVIDER stations of each provider,
walking every provider in sorted order. The scope is therefore *deterministic*
(all providers x STATIONS_PER_PROVIDER stations) rather than "whatever fit in N
seconds" — no self-imposed wall-clock budget. Per-request timeouts + bounded
retries cap a slow/hostile provider, and the supervisor is the only wall-clock
backstop (if a run is interrupted, this stateless connector simply re-runs the
same deterministic scope next time). Each series is pulled for the last
LOOKBACK_DAYS of *its own* period of record (anchored to the series end, not to
"now") — so feeds that lag by a year or two still yield their most recent data,
and every GetValues stays small and fast.
"""

import html
import re
from datetime import datetime, timedelta, timezone

import httpx
import pyarrow as pa
from tenacity import (
    retry,
    retry_if_exception,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    raw_parquet_writer,
)
from utils import (
    META_PAGE,
    _WOF_URL,
    _SITEINFO_URL,
    _is_transient,
    _list_providers,
    _members,
    _to_naive_utc,
)

# Crawl tuning.
LOOKBACK_DAYS = 365          # per-series window, anchored to the series' end
STATIONS_PER_PROVIDER = 3    # breadth over depth: sample N stations per provider

_VALUES_SCHEMA = pa.schema([
    ("provider", pa.string()),
    ("timeseries_id", pa.string()),
    ("station_id", pa.string()),
    ("variable_code", pa.string()),
    ("variable_name", pa.string()),
    ("unit", pa.string()),
    ("observed_at", pa.timestamp("s")),
    ("value", pa.float64()),
])


# --------------------------------------------------------------------------- #
# values — WaterOneFlow GetSiteInfo + GetValues, station-driven
# --------------------------------------------------------------------------- #

def _value_window(begin_str, end_str, now):
    """Last LOOKBACK_DAYS of a series' own period of record. Anchored to the
    series end (not 'now') so lagging feeds still return their most recent data,
    and each GetValues stays ~1 year and fast. Returns (start, end) as
    YYYY-MM-DD, or (None, None) if empty."""
    begin = _to_naive_utc(begin_str)
    end = _to_naive_utc(end_str) or now
    if end > now:
        end = now
    start = end - timedelta(days=LOOKBACK_DAYS)
    if begin and begin > start:
        start = begin
    if start >= end:
        return None, None
    return start.strftime("%Y-%m-%d"), end.strftime("%Y-%m-%d")


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(1),   # a slow GetValues won't get faster on retry —
    reraise=True,                 # fail fast and skip, don't burn the budget
)
def _get_values_xml(location: str, variable: str, start: str, end: str) -> str:
    resp = get(
        _WOF_URL,
        params={"location": location, "variable": variable,
                "startDate": start, "endDate": end, "authToken": ""},
        timeout=(10.0, 40.0),
    )
    resp.raise_for_status()
    return resp.text


def _series_values(provider, station, variable, start, end):
    """WaterOneFlow GetValues -> [(datetime_str, value_str)], nodata dropped."""
    x = html.unescape(_get_values_xml(f"{provider}:{station}", f"{provider}:{variable}", start, end))
    nodata = set(re.findall(r"<noDataValue>([^<]+)</noDataValue>", x))
    out = []
    for attrs, val in re.findall(r"<value([^>]*)>([^<]*)</value>", x):
        if not val or val in nodata:
            continue
        m = re.search(r'dateTimeUTC="([^"]+)"', attrs) or re.search(r'dateTime="([^"]+)"', attrs)
        if m:
            out.append((m.group(1), val))
    return out


@retry(
    retry=retry_if_exception(_is_transient),
    stop=stop_after_attempt(2),
    wait=wait_exponential(min=4, max=15),
    reraise=True,
)
def _get_siteinfo_xml(site: str) -> str:
    resp = get(_SITEINFO_URL, params={"site": site, "authToken": ""}, timeout=(10.0, 40.0))
    resp.raise_for_status()
    return resp.text


def _site_series(provider, station):
    """GetSiteInfo -> the station's series catalog as
    [{variable_code, variable_name, unit, begin, end}]. variable_code is the
    WaterOneFlow-native code GetValues accepts (the timeseries-api observedProperty
    href is often a GetValues-incompatible ontology concept URI)."""
    x = html.unescape(_get_siteinfo_xml(f"{provider}:{station}"))
    out = []
    for block in re.findall(r"<series>(.*?)</series>", x, re.S):
        vc = re.search(r"<variableCode[^>]*>([^<]+)</variableCode>", block)
        if not vc:
            continue
        vn = re.search(r"<variableName[^>]*>([^<]*)</variableName>", block)
        un = re.search(r"<unitName[^>]*>([^<]*)</unitName>", block)
        bt = re.search(r"<beginDateTime[^>]*>([^<]+)</beginDateTime>", block)
        et = re.search(r"<endDateTime[^>]*>([^<]+)</endDateTime>", block)
        out.append({
            "variable_code": vc.group(1),
            "variable_name": vn.group(1) if vn else None,
            "unit": un.group(1) if un else None,
            "begin": bt.group(1) if bt else None,
            "end": et.group(1) if et else None,
        })
    return out


def _provider_stations(provider, cap):
    """First `cap` distinct station ids of a provider (from the metadata
    endpoint). Bounds enumeration so a huge provider doesn't cost a full scan."""
    seen = set()
    order = []
    offset = 1
    while len(order) < cap:
        members = _members(provider, offset, META_PAGE)
        for m in members:
            st = (m.get("featureOfInterest") or {}).get("href")
            if st and st not in seen:
                seen.add(st)
                order.append(st)
                if len(order) >= cap:
                    break
        if len(members) < META_PAGE:
            break
        offset += META_PAGE
    return order


def _write_provider_values(asset_id, provider, stations, now) -> None:
    """Stream one provider's sampled stations' observations to a parquet batch,
    one series at a time (bounded memory)."""
    writer_cm = None
    writer = None
    try:
        for station in stations:
            try:
                series = _site_series(provider, station)
            except httpx.HTTPError as exc:
                print(f"[wmo-values] skip siteinfo {provider}:{station}: {type(exc).__name__}")
                continue
            for s in series:
                vc = s["variable_code"]
                start, stop = _value_window(s["begin"], s["end"], now)
                if start is None:
                    continue
                try:
                    pairs = _series_values(provider, station, vc, start, stop)
                except httpx.HTTPError as exc:
                    print(f"[wmo-values] skip {provider}:{station}/{vc}: {type(exc).__name__}")
                    continue
                rows = []
                for dt_str, raw_val in pairs:
                    observed_at = _to_naive_utc(dt_str)
                    if observed_at is None:
                        continue
                    try:
                        value = float(raw_val)
                    except (TypeError, ValueError):
                        continue
                    rows.append({
                        "provider": provider,
                        "timeseries_id": f"{station}:{vc}",
                        "station_id": station,
                        "variable_code": vc,
                        "variable_name": s["variable_name"],
                        "unit": s["unit"],
                        "observed_at": observed_at,
                        "value": value,
                    })
                if not rows:
                    continue
                table = pa.Table.from_pylist(rows, schema=_VALUES_SCHEMA)
                if writer is None:
                    writer_cm = raw_parquet_writer(asset_id, _VALUES_SCHEMA)
                    writer = writer_cm.__enter__()
                writer.write_table(table)
    finally:
        if writer_cm is not None:
            writer_cm.__exit__(None, None, None)


def fetch_values(node_id: str) -> None:
    asset = node_id  # "wmo-values"
    now = datetime.now(tz=timezone.utc).replace(tzinfo=None)

    try:
        providers = _list_providers()
    except httpx.HTTPError as exc:
        print(f"[wmo-values] provider enumeration failed: {type(exc).__name__}")
        return

    # Deterministic scope: every provider x STATIONS_PER_PROVIDER stations. No
    # per-run/per-provider time cap — request timeouts bound slow providers and
    # the supervisor bounds the run.
    for provider in providers:
        try:
            stations = _provider_stations(provider, STATIONS_PER_PROVIDER)
        except httpx.HTTPError as exc:
            print(f"[wmo-values] skip provider {provider} (enum): {type(exc).__name__}")
            continue
        if not stations:
            continue
        if len(stations) >= STATIONS_PER_PROVIDER:
            print(f"[wmo-values] {provider}: sampling first {STATIONS_PER_PROVIDER} stations")
        # Pure batch coordinate: the provider.
        _write_provider_values(f"{asset}-{provider}", provider, stations, now)


DOWNLOAD_SPECS = [
    NodeSpec(id="wmo-values", fn=fetch_values, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="wmo-values-transform",
        deps=["wmo-values"],
        sql='''
            SELECT
                provider,
                timeseries_id,
                station_id,
                variable_code,
                variable_name,
                unit,
                CAST(observed_at AS TIMESTAMP) AS observed_at,
                CAST(value AS DOUBLE)          AS value
            FROM (
                SELECT *, row_number() OVER (
                    PARTITION BY provider, station_id, variable_code, observed_at
                    ORDER BY value
                ) AS _rn
                FROM "wmo-values"
                WHERE observed_at IS NOT NULL
                  AND value IS NOT NULL
            )
            WHERE _rn = 1
        ''',
    ),
]
