"""IBGE aggregate time series — parametric download + transform.

Catalog connector over the IBGE agregados v3 API (servicodados). Each accepted
aggregate (statistical table) is fetched as a bounded national/regional headline
time series: all variables, all periods, at the smallest territorial level the
table supports (prefer state N3 > region N2 > Brazil N1), default classification
aggregate only (requesting every classification category 500s on the server).
One published Delta table per aggregate. Uniform long-format schema across every
aggregate subset — a single parametric fetcher driven by ``ENTITY_IDS``.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import get_json

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


# The accepted aggregate ids (rank >= publish threshold), inlined — no
# module-level I/O. Source of truth: data/sources/ibge/work/entity_union.json.
from constants import ENTITY_IDS

DOWNLOAD_SPECS = [
    NodeSpec(id=f"ibge-{eid}", fn=fetch_aggregate, kind="download")
    for eid in ENTITY_IDS
]


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


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"ibge-{eid}-transform",
        fn=None,
        kind="transform",
        deps=(f"ibge-{eid}",),
        sql=_agg_sql(f"ibge-{eid}"),
    )
    for eid in ENTITY_IDS
]
