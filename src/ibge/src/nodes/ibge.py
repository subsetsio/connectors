"""IBGE connector — agregados v3 time series + a municipality geography table.

Two fetch shapes share one host (servicodados.ibge.gov.br):

1. **Aggregates** (catalog, ~500 entities). Each accepted aggregate (statistical
   table) is fetched as a bounded long-format headline time series: all variables,
   all periods, at the smallest territorial level the table supports (prefer state
   N3 > region N2 > Brazil N1), default classification aggregate only (requesting
   every classification category 500s on the server). One published Delta table
   per aggregate, uniform long-format schema. Driven by ``ENTITY_IDS``.

2. **Municipios** (single reference table). Flattens the Brazilian municipality
   hierarchy (municipio -> microrregiao -> mesorregiao -> UF -> regiao) from the
   localidades v1 API.

Stateless full re-pull every run: the agregados API has no changed-since filter,
each accepted table is a bounded national/regional series, and revisions are
picked up for free by never trusting a stored watermark.

IBGE's servers silently drop the library's default datacenter User-Agent from
cloud egress IPs (works from a browser-like client; the first cloud run timed out
on every request), so all requests go through ``get_json`` with browser-like
headers and a generous transient-retry policy.
"""

import httpx
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_exponential,
)

from subsets_utils import NodeSpec, SqlNodeSpec, get, save_raw_ndjson

from constants import ENTITY_IDS


# --- shared HTTP -----------------------------------------------------------

class _Transient(Exception):
    """Retryable upstream condition (5xx / overload)."""


# servicodados silently drops the default datacenter User-Agent from cloud
# egress IPs (works from a browser-like client). Present as a normal browser
# and accept Brazilian JSON. ASCII-only header values.
_HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    ),
    "Accept": "application/json",
    "Accept-Language": "pt-BR,pt;q=0.9,en;q=0.8",
}

# Short connect timeout so a dropped connection fails fast and leaves room for
# more attempts; generous read timeout because a few aggregates return large
# series.
_TIMEOUT = httpx.Timeout(connect=15.0, read=60.0, write=60.0, pool=15.0)


@retry(
    retry=retry_if_exception_type(
        (_Transient, httpx.TransportError, httpx.TimeoutException)
    ),
    wait=wait_exponential(multiplier=2, max=30),
    stop=stop_after_attempt(6),
    reraise=True,
)
def get_json(url: str):
    resp = get(url, timeout=_TIMEOUT, headers=_HEADERS)
    if resp.status_code >= 500:
        raise _Transient(f"{resp.status_code} for {url}")
    resp.raise_for_status()
    return resp.json()


# --- aggregates ------------------------------------------------------------

_AGG = "https://servicodados.ibge.gov.br/api/v3/agregados"
# Smallest-cardinality administrative levels, richest-but-bounded first. Every
# accepted aggregate supports at least one of these (rank gated on it), so each
# fetch returns at most ~27 localities (states) x periods x variables.
_LEVEL_PREF = ("N3", "N2", "N1")


def _pick_level(administrativo) -> str:
    for level in _LEVEL_PREF:
        if level in (administrativo or []):
            return level
    # Rank restricted the accepted set to tables exposing N1/N2/N3; fall back to
    # Brazil-level if upstream metadata ever disagrees.
    return "N1"


def fetch_aggregate(node_id: str) -> None:
    """Fetch one IBGE aggregate as a long-format headline time series."""
    agg = node_id[len("ibge-"):]
    meta = get_json(f"{_AGG}/{agg}/metadados")
    var_ids = [v["id"] for v in meta.get("variaveis", [])]
    if not var_ids:
        raise ValueError(f"{node_id}: aggregate {agg} exposes no variaveis")
    level = _pick_level((meta.get("nivelTerritorial") or {}).get("Administrativo"))
    var_path = "|".join(str(v) for v in var_ids)
    url = (
        f"{_AGG}/{agg}/periodos/all/variaveis/{var_path}"
        f"?localidades={level}[all]"
    )
    data = get_json(url)

    rows = []
    for result in data:
        var_id = result.get("id")
        var_name = result.get("variavel")
        unidade = result.get("unidade")
        for bloc in result.get("resultados", []):
            cat_names = []
            for clf in bloc.get("classificacoes", []):
                cat_names.extend((clf.get("categoria") or {}).values())
            categoria = " / ".join(n for n in cat_names if n)
            for serie in bloc.get("series", []):
                loc = serie.get("localidade") or {}
                nivel = (loc.get("nivel") or {}).get("id")
                for periodo, valor in (serie.get("serie") or {}).items():
                    rows.append({
                        "aggregado": agg,
                        "variavel_id": var_id,
                        "variavel": var_name,
                        "unidade": unidade,
                        "nivel": nivel,
                        "localidade_id": loc.get("id"),
                        "localidade": loc.get("nome"),
                        "periodo": periodo,
                        "categoria": categoria,
                        "valor": valor,
                    })
    save_raw_ndjson(rows, node_id)


def _agg_sql(asset_id: str) -> str:
    return (
        "SELECT "
        "aggregado, "
        "CAST(variavel_id AS BIGINT) AS variavel_id, "
        "variavel, unidade, nivel, "
        "CAST(localidade_id AS VARCHAR) AS localidade_id, localidade, "
        "CAST(periodo AS VARCHAR) AS periodo, "
        "NULLIF(categoria, '') AS categoria, "
        "TRY_CAST(valor AS DOUBLE) AS valor "
        f'FROM "{asset_id}"'
    )


# --- municipios reference table -------------------------------------------

_MUNI = "https://servicodados.ibge.gov.br/api/v1/localidades/municipios"


def fetch_municipios(node_id: str) -> None:
    """Fetch the Brazilian municipality geography reference table."""
    data = get_json(_MUNI)
    rows = []
    for m in data:
        micro = m.get("microrregiao") or {}
        meso = micro.get("mesorregiao") or {}
        uf = meso.get("UF") or {}
        regiao = uf.get("regiao") or {}
        rows.append({
            "municipio_id": str(m.get("id")),
            "municipio": m.get("nome"),
            "microrregiao_id": micro.get("id"),
            "microrregiao": micro.get("nome"),
            "mesorregiao_id": meso.get("id"),
            "mesorregiao": meso.get("nome"),
            "uf_id": uf.get("id"),
            "uf_sigla": uf.get("sigla"),
            "uf": uf.get("nome"),
            "regiao_id": regiao.get("id"),
            "regiao_sigla": regiao.get("sigla"),
            "regiao": regiao.get("nome"),
        })
    save_raw_ndjson(rows, node_id)


_MUNI_SQL = (
    "SELECT "
    "municipio_id, municipio, "
    "CAST(microrregiao_id AS BIGINT) AS microrregiao_id, microrregiao, "
    "CAST(mesorregiao_id AS BIGINT) AS mesorregiao_id, mesorregiao, "
    "CAST(uf_id AS BIGINT) AS uf_id, uf_sigla, uf, "
    "CAST(regiao_id AS BIGINT) AS regiao_id, regiao_sigla, regiao "
    'FROM "ibge-municipios"'
)


# --- DAG -------------------------------------------------------------------
# ENTITY_IDS is the rank-accepted entity union (incl. "municipios"); the
# numeric aggregate ids fan out over fetch_aggregate, municipios gets its own fn.

_AGG_IDS = [eid for eid in ENTITY_IDS if eid != "municipios"]

DOWNLOAD_SPECS = [
    NodeSpec(id=f"ibge-{eid}", fn=fetch_aggregate, kind="download")
    for eid in _AGG_IDS
] + [
    NodeSpec(id="ibge-municipios", fn=fetch_municipios, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"ibge-{eid}-transform",
        fn=None,
        kind="transform",
        deps=(f"ibge-{eid}",),
        sql=_agg_sql(f"ibge-{eid}"),
    )
    for eid in _AGG_IDS
] + [
    SqlNodeSpec(
        id="ibge-municipios-transform",
        fn=None,
        kind="transform",
        deps=("ibge-municipios",),
        sql=_MUNI_SQL,
    ),
]
