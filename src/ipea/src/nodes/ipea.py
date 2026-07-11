"""IPEA / IPEADATA connector.

Source: IPEADATA OData v4 API (http://www.ipeadata.gov.br/api/odata4/).
The chosen mechanism is the partial-OData REST endpoint: the full series
catalog (/Metadados, ~3600 numeric series) returns in one request, and each
series' observations are fetched individually via /ValoresSerie(SERCODIGO='X').

Two published subsets:
  - ipea-series : the series metadata catalog (one row per SERCODIGO).
  - ipea-values : long-format observations across ALL series. Regional-base
    series carry per-territory breakdowns (NIVNOME/TERCODIGO populated), so the
    combined corpus is large (~100M rows). It is streamed per series with a
    bounded-memory parquet writer.

Fetch shape: stateless full re-pull. The API exposes no usable `since` filter
for whole-corpus extraction, and the catalog is re-pullable each run, so we
re-fetch everything and overwrite — revisions are picked up for free.
"""

import httpx
import pyarrow as pa

from subsets_utils import (
    NodeSpec,
    get,
    transient_retry,
    save_raw_parquet,
    raw_parquet_writer,
)

# HTTPS: the plain-HTTP (port 80) endpoint is dropped from cloud runners and
# does not redirect to https, so we must request https directly.
BASE = "https://www.ipeadata.gov.br/api/odata4"

# Generous read timeout: some Regional series return hundreds of thousands of
# rows in a single response. Short connect/write so dead connections fail fast
# and transient_retry can back off.
TIMEOUT = httpx.Timeout(connect=15.0, read=300.0, write=60.0, pool=60.0)

# Metadados catalog fields (one record per series).
META_FIELDS = [
    "SERCODIGO", "SERNOME", "SERCOMENTARIO", "SERATUALIZACAO", "BASNOME",
    "FNTSIGLA", "FNTNOME", "FNTURL", "PERNOME", "UNINOME", "MULNOME",
    "SERSTATUS", "PAICODIGO",
]

SERIES_SCHEMA = pa.schema(
    [(f, pa.string()) for f in META_FIELDS]
    + [("TEMCODIGO", pa.int64()), ("SERNUMERICA", pa.bool_())]
)

VALUES_SCHEMA = pa.schema([
    ("SERCODIGO", pa.string()),
    ("VALDATA", pa.string()),     # raw ISO8601 string; cast to DATE in transform
    ("VALVALOR", pa.float64()),   # nullable — some observations have no value
    ("NIVNOME", pa.string()),     # geographic level (Regional-base series)
    ("TERCODIGO", pa.string()),   # territory code (Regional-base series)
])

THEMES_SCHEMA = pa.schema([
    ("TEMCODIGO", pa.int64()),
    ("TEMCODIGO_PAI", pa.int64()),
    ("TEMNOME", pa.string()),
])

TERRITORIES_SCHEMA = pa.schema([
    ("NIVNOME", pa.string()),
    ("TERCODIGO", pa.string()),
    ("TERNOME", pa.string()),
    ("TERNOMEPADRAO", pa.string()),
    ("TERCAPITAL", pa.int64()),
    ("TERAREA", pa.float64()),
    ("NIVAMC", pa.bool_()),
])


@transient_retry()
def _get_json(url: str):
    resp = get(url, timeout=TIMEOUT)
    resp.raise_for_status()
    return resp.json()


def _fetch_metadados() -> list[dict]:
    """The entire series catalog in one request (no pagination)."""
    return _get_json(f"{BASE}/Metadados")["value"]


def fetch_series(node_id: str) -> None:
    """ipea-series — the series metadata catalog."""
    asset = node_id
    rows = _fetch_metadados()
    table = pa.Table.from_pylist(
        [{
            "SERCODIGO": r.get("SERCODIGO"),
            "SERNOME": r.get("SERNOME"),
            "SERCOMENTARIO": r.get("SERCOMENTARIO"),
            "SERATUALIZACAO": r.get("SERATUALIZACAO"),
            "BASNOME": r.get("BASNOME"),
            "FNTSIGLA": r.get("FNTSIGLA"),
            "FNTNOME": r.get("FNTNOME"),
            "FNTURL": r.get("FNTURL"),
            "PERNOME": r.get("PERNOME"),
            "UNINOME": r.get("UNINOME"),
            "MULNOME": r.get("MULNOME"),
            "SERSTATUS": r.get("SERSTATUS"),
            "PAICODIGO": r.get("PAICODIGO"),
            "TEMCODIGO": r.get("TEMCODIGO"),
            "SERNUMERICA": r.get("SERNUMERICA"),
        } for r in rows],
        schema=SERIES_SCHEMA,
    )
    save_raw_parquet(table, asset)


def fetch_values(node_id: str) -> None:
    """ipea-values — long-format observations across every series.

    Streamed per series so peak memory is bounded by the largest single
    series response, not the whole corpus.
    """
    asset = node_id
    codes = [r["SERCODIGO"] for r in _fetch_metadados() if r.get("SERCODIGO")]
    written = 0
    with raw_parquet_writer(asset, VALUES_SCHEMA) as writer:
        for code in codes:
            # Single-quote string key in the OData function call.
            url = f"{BASE}/ValoresSerie(SERCODIGO='{code}')"
            values = _get_json(url)["value"]
            if not values:
                continue
            table = pa.Table.from_pylist(
                [{
                    "SERCODIGO": v.get("SERCODIGO") or code,
                    "VALDATA": v.get("VALDATA"),
                    "VALVALOR": v.get("VALVALOR"),
                    "NIVNOME": v.get("NIVNOME"),
                    "TERCODIGO": v.get("TERCODIGO"),
                } for v in values],
                schema=VALUES_SCHEMA,
            )
            writer.write_table(table)
            written += 1
    if written == 0:
        raise AssertionError("ipea-values: no series returned any observations")


def fetch_themes(node_id: str) -> None:
    """ipea-themes — hierarchical subject taxonomy for series metadata."""
    rows = _get_json(f"{BASE}/Temas")["value"]
    table = pa.Table.from_pylist(
        [{
            "TEMCODIGO": r.get("TEMCODIGO"),
            "TEMCODIGO_PAI": r.get("TEMCODIGO_PAI"),
            "TEMNOME": r.get("TEMNOME"),
        } for r in rows],
        schema=THEMES_SCHEMA,
    )
    save_raw_parquet(table, node_id)


def fetch_territories(node_id: str) -> None:
    """ipea-territories — geographic dimension used by Regional series."""
    rows = _get_json(f"{BASE}/Territorios")["value"]
    table = pa.Table.from_pylist(
        [{
            "NIVNOME": r.get("NIVNOME"),
            "TERCODIGO": r.get("TERCODIGO"),
            "TERNOME": r.get("TERNOME"),
            "TERNOMEPADRAO": r.get("TERNOMEPADRAO"),
            "TERCAPITAL": r.get("TERCAPITAL"),
            "TERAREA": r.get("TERAREA"),
            "NIVAMC": r.get("NIVAMC"),
        } for r in rows],
        schema=TERRITORIES_SCHEMA,
    )
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ipea-series", fn=fetch_series, kind="download"),
    NodeSpec(id="ipea-territories", fn=fetch_territories, kind="download"),
    NodeSpec(id="ipea-themes", fn=fetch_themes, kind="download"),
    NodeSpec(id="ipea-values", fn=fetch_values, kind="download"),
]
