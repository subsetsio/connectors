"""Central Electricity Authority (India) — native JSON API connector.

Mechanism: rest_json. Each endpoint at https://cea.nic.in/api/<name>.php is a
full-table dump of one statistical time series (no auth, no pagination, no
incremental filter — query params are ignored). We re-fetch every endpoint in
full each run (stateless full re-pull; total corpus ~4-5 MB) and overwrite.

Raw is saved as NDJSON: numeric fields arrive as quoted strings (some empty,
some null), `id` is sometimes int / sometimes string, and column sets differ
per endpoint — heterogeneous enough that a fixed parquet schema would be
brittle. The per-endpoint TRANSFORM_SPECS do the typing: parse the `Mon-YYYY`
period to a DATE and TRY_CAST the value columns to DOUBLE.
"""

import certifi

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    configure_http,
    get,
    save_raw_ndjson,
    transient_retry,
)

PREFIX = "central-electricity-authority-"
BASE = "https://cea.nic.in/api/"

# cea.nic.in serves an INCOMPLETE TLS chain: it presents only the leaf cert and
# omits the "RapidSSL TLS RSA CA G1" intermediate, so httpx/certifi can't build
# a path to the trusted root (DigiCert Global Root G2) and raises
# CERTIFICATE_VERIFY_FAILED. The intermediate is a stable, well-known DigiCert
# CA; we embed it here and splice it into the certifi bundle that httpx loads,
# once per process, rather than disabling verification (no verify=False).
_RAPIDSSL_INTERMEDIATE_PEM = """-----BEGIN CERTIFICATE-----
MIIEszCCA5ugAwIBAgIQCyWUIs7ZgSoVoE6ZUooO+jANBgkqhkiG9w0BAQsFADBh
MQswCQYDVQQGEwJVUzEVMBMGA1UEChMMRGlnaUNlcnQgSW5jMRkwFwYDVQQLExB3
d3cuZGlnaWNlcnQuY29tMSAwHgYDVQQDExdEaWdpQ2VydCBHbG9iYWwgUm9vdCBH
MjAeFw0xNzExMDIxMjI0MzNaFw0yNzExMDIxMjI0MzNaMGAxCzAJBgNVBAYTAlVT
MRUwEwYDVQQKEwxEaWdpQ2VydCBJbmMxGTAXBgNVBAsTEHd3dy5kaWdpY2VydC5j
b20xHzAdBgNVBAMTFlJhcGlkU1NMIFRMUyBSU0EgQ0EgRzEwggEiMA0GCSqGSIb3
DQEBAQUAA4IBDwAwggEKAoIBAQC/uVklRBI1FuJdUEkFCuDL/I3aJQiaZ6aibRHj
ap/ap9zy1aYNrphe7YcaNwMoPsZvXDR+hNJOo9gbgOYVTPq8gXc84I75YKOHiVA4
NrJJQZ6p2sJQyqx60HkEIjzIN+1LQLfXTlpuznToOa1hyTD0yyitFyOYwURM+/CI
8FNFMpBhw22hpeAQkOOLmsqT5QZJYeik7qlvn8gfD+XdDnk3kkuuu0eG+vuyrSGr
5uX5LRhFWlv1zFQDch/EKmd163m6z/ycx/qLa9zyvILc7cQpb+k7TLra9WE17YPS
n9ANjG+ECo9PDW3N9lwhKQCNvw1gGoguyCQu7HE7BnW8eSSFAgMBAAGjggFmMIIB
YjAdBgNVHQ4EFgQUDNtsgkkPSmcKuBTuesRIUojrVjgwHwYDVR0jBBgwFoAUTiJU
IBiV5uNu5g/6+rkS7QYXjzkwDgYDVR0PAQH/BAQDAgGGMB0GA1UdJQQWMBQGCCsG
AQUFBwMBBggrBgEFBQcDAjASBgNVHRMBAf8ECDAGAQH/AgEAMDQGCCsGAQUFBwEB
BCgwJjAkBggrBgEFBQcwAYYYaHR0cDovL29jc3AuZGlnaWNlcnQuY29tMEIGA1Ud
HwQ7MDkwN6A1oDOGMWh0dHA6Ly9jcmwzLmRpZ2ljZXJ0LmNvbS9EaWdpQ2VydEds
b2JhbFJvb3RHMi5jcmwwYwYDVR0gBFwwWjA3BglghkgBhv1sAQEwKjAoBggrBgEF
BQcCARYcaHR0cHM6Ly93d3cuZGlnaWNlcnQuY29tL0NQUzALBglghkgBhv1sAQIw
CAYGZ4EMAQIBMAgGBmeBDAECAjANBgkqhkiG9w0BAQsFAAOCAQEAGUSlOb4K3Wtm
SlbmE50UYBHXM0SKXPqHMzk6XQUpCheF/4qU8aOhajsyRQFDV1ih/uPIg7YHRtFi
CTq4G+zb43X1T77nJgSOI9pq/TqCwtukZ7u9VLL3JAq3Wdy2moKLvvC8tVmRzkAe
0xQCkRKIjbBG80MSyDX/R4uYgj6ZiNT/Zg6GI6RofgqgpDdssLc0XIRQEotxIZcK
zP3pGJ9FCbMHmMLLyuBd+uCWvVcF2ogYAawufChS/PT61D9rqzPRS5I2uqa3tmIT
44JhJgWhBnFMb7AGQkvNq9KNS9dd3GWc17H/dXa1enoxzWjE0hBdFjxPhUb0W3wi
8o34/m8Fxw==
-----END CERTIFICATE-----"""

_CA_PATCHED = False


def _ensure_ca_chain() -> None:
    """Splice the missing intermediate into certifi's bundle (idempotent) and
    reset the shared httpx client so it rebuilds its SSL context from the
    patched bundle. Runs once per process, inside a fetch fn (no module I/O)."""
    global _CA_PATCHED
    if _CA_PATCHED:
        return
    bundle = certifi.where()
    with open(bundle, "r", encoding="ascii") as fh:
        current = fh.read()
    if _RAPIDSSL_INTERMEDIATE_PEM not in current:
        with open(bundle, "a", encoding="ascii") as fh:
            fh.write("\n" + _RAPIDSSL_INTERMEDIATE_PEM + "\n")
        configure_http()  # drop the cached client so it reloads the CA bundle
    _CA_PATCHED = True


# spec-id suffix (entity_id, already lowercase-hyphen) -> exact endpoint php
# basename (the URL is case-sensitive; note `percapitalConsumtion` is camelCase
# upstream).
_SUFFIX_TO_ENDPOINT = {
    "installed-capacity-allindia": "installed_capacity_allindia",
    "installed-capacity-allindia-res": "instcap_allindia_res",
    "installed-capacity-regionwise": "installed_capacity",
    "installed-capacity-statewise": "installed_capacity_statewise",
    "per-capita-consumption": "percapitalConsumtion",
    "power-generation": "power_generation",
    "power-supply-position-energy": "psp_energy",
    "power-supply-position-peak": "psp_peak",
    "renewable-energy-generation": "renewable_energy",
    "transmission-lines": "transmission_lines",
    "transformation-capacity": "transformation_substations",
}

ENTITY_IDS = list(_SUFFIX_TO_ENDPOINT.keys())


@transient_retry()
def _fetch(url: str):
    # Content-Type is text/javascript but the body is valid JSON; httpx's
    # .json() parses the bytes regardless of the declared content type.
    resp = get(url, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _flatten(payload) -> list:
    """Normalize both response shapes to a flat list of row dicts.

    Time-series endpoints (psp_energy, psp_peak, power_generation,
    renewable_energy) return an object keyed by financial year whose values are
    arrays of rows; capacity-snapshot endpoints return a flat array.
    """
    rows: list = []
    if isinstance(payload, dict):
        for v in payload.values():
            if isinstance(v, list):
                rows.extend(r for r in v if isinstance(r, dict))
            elif isinstance(v, dict):
                rows.append(v)
    elif isinstance(payload, list):
        rows = [r for r in payload if isinstance(r, dict)]
    return rows


def fetch_one(node_id: str) -> None:
    _ensure_ca_chain()
    asset = node_id  # the spec id IS the asset name
    suffix = node_id[len(PREFIX):]
    endpoint = _SUFFIX_TO_ENDPOINT[suffix]
    payload = _fetch(BASE + endpoint + ".php")
    rows = _flatten(payload)
    if not rows:
        raise ValueError(f"{node_id}: endpoint {endpoint}.php returned no rows")
    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=PREFIX + eid, fn=fetch_one, kind="download")
    for eid in ENTITY_IDS
]

# Shared fuel-capacity column projection (installed-capacity family is wide:
# one MW column per fuel). All values are quoted strings -> TRY_CAST to DOUBLE.
_FUEL_COLS = """
        TRY_CAST(coal AS DOUBLE)          AS coal_mw,
        TRY_CAST(gas AS DOUBLE)           AS gas_mw,
        TRY_CAST(diesel AS DOUBLE)        AS diesel_mw,
        TRY_CAST(thermal_total AS DOUBLE) AS thermal_total_mw,
        TRY_CAST(nuclear AS DOUBLE)       AS nuclear_mw,
        TRY_CAST(hydro AS DOUBLE)         AS hydro_mw,
        TRY_CAST(res AS DOUBLE)           AS res_mw
"""

# Per-download SQL. The dep id is registered as a view of the same name; raw
# columns are referenced case-insensitively (unquoted). `try_strptime` parses
# the 'Mon-YYYY' period and yields NULL (not an error) on any odd format.
_SQL = {
    PREFIX + "installed-capacity-allindia": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
{_FUEL_COLS},
            TRY_CAST(grand_total AS DOUBLE) AS total_mw
        FROM "{PREFIX}installed-capacity-allindia"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "installed-capacity-regionwise": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            trim(region) AS region,
{_FUEL_COLS},
            TRY_CAST(total AS DOUBLE) AS total_mw
        FROM "{PREFIX}installed-capacity-regionwise"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "installed-capacity-statewise": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            trim(region) AS region,
            trim(state) AS state,
{_FUEL_COLS},
            TRY_CAST(grand_total AS DOUBLE) AS total_mw
        FROM "{PREFIX}installed-capacity-statewise"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "installed-capacity-allindia-res": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            TRY_CAST(small_hydro_power AS DOUBLE) AS small_hydro_mw,
            TRY_CAST(wind_power AS DOUBLE)        AS wind_mw,
            TRY_CAST(bmpower_congen AS DOUBLE)    AS biomass_cogen_mw,
            TRY_CAST(wastetoenergy AS DOUBLE)     AS waste_to_energy_mw,
            TRY_CAST(solar_power AS DOUBLE)       AS solar_mw
        FROM "{PREFIX}installed-capacity-allindia-res"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    # `region_state` is constant ("All India") on this endpoint, so it is
    # dropped; the series is keyed by month x mode.
    PREFIX + "power-generation": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            fy AS financial_year,
            trim(mode) AS mode,
            TRY_CAST(bus AS DOUBLE) AS bus_energy
        FROM "{PREFIX}power-generation"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "renewable-energy-generation": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            fy AS financial_year,
            trim(state) AS state,
            trim(region) AS region,
            TRY_CAST(wind AS DOUBLE)        AS wind,
            TRY_CAST(solar AS DOUBLE)       AS solar,
            TRY_CAST(biomass AS DOUBLE)     AS biomass,
            TRY_CAST(bagasse AS DOUBLE)     AS bagasse,
            TRY_CAST(small_hydel AS DOUBLE) AS small_hydel,
            TRY_CAST(others AS DOUBLE)      AS others,
            TRY_CAST(total AS DOUBLE)       AS total
        FROM "{PREFIX}renewable-energy-generation"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "power-supply-position-peak": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            fy AS financial_year,
            trim(state) AS state,
            TRY_CAST(peak_demand AS DOUBLE) AS peak_demand_mw,
            TRY_CAST(peak_met AS DOUBLE)    AS peak_met_mw
        FROM "{PREFIX}power-supply-position-peak"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "power-supply-position-energy": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            fy AS financial_year,
            trim(state) AS state,
            TRY_CAST(energy_requirement AS DOUBLE)  AS energy_requirement_mu,
            TRY_CAST(energy_availability AS DOUBLE) AS energy_availability_mu
        FROM "{PREFIX}power-supply-position-energy"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "transmission-lines": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            TRY_CAST(voltage_level AS INTEGER) AS voltage_level_kv,
            trim(transmission_line) AS transmission_line,
            trim(circuit_type) AS circuit_type,
            trim(executing_agency) AS executing_agency,
            trim(sector) AS sector,
            TRY_CAST(line_length AS DOUBLE) AS line_length_ckm
        FROM "{PREFIX}transmission-lines"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "transformation-capacity": f'''
        SELECT
            try_strptime(month, '%b-%Y')::DATE AS month,
            trim(voltage_ratio) AS voltage_ratio,
            trim(station_name) AS station_name,
            TRY_CAST(capacity AS DOUBLE) AS capacity_mva,
            trim(executing_agency) AS executing_agency,
            trim(sector) AS sector
        FROM "{PREFIX}transformation-capacity"
        WHERE month IS NOT NULL AND month <> ''
    ''',
    PREFIX + "per-capita-consumption": f'''
        SELECT
            trim("Year") AS financial_year,
            TRY_CAST(split_part(trim("Year"), '-', 1) AS INTEGER) AS year_start,
            trim(state) AS state,
            TRY_CAST(value AS DOUBLE) AS per_capita_consumption_kwh
        FROM "{PREFIX}per-capita-consumption"
        WHERE "Year" IS NOT NULL AND "Year" <> ''
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(id=f"{s.id}-transform", deps=[s.id], sql=_SQL[s.id])
    for s in DOWNLOAD_SPECS
]
