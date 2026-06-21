"""IBGE municipality geography reference table — download + transform.

A single reference table flattening the Brazilian municipality hierarchy
(municipio -> microrregiao -> mesorregiao -> UF -> regiao) from the localidades
v1 API. Distinct endpoint, parse, and schema from the aggregate time series.
"""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import get_json

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


DOWNLOAD_SPECS = [
    NodeSpec(id="ibge-municipios", fn=fetch_municipios, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ibge-municipios-transform",
        fn=None,
        kind="transform",
        deps=("ibge-municipios",),
        sql=(
            "SELECT "
            "municipio_id, municipio, "
            "CAST(microrregiao_id AS BIGINT) AS microrregiao_id, microrregiao, "
            "CAST(mesorregiao_id AS BIGINT) AS mesorregiao_id, mesorregiao, "
            "CAST(uf_id AS BIGINT) AS uf_id, uf_sigla, uf, "
            "CAST(regiao_id AS BIGINT) AS regiao_id, regiao_sigla, regiao "
            'FROM "ibge-municipios"'
        ),
    ),
]
