"""Expectativas (Focus survey) — Olinda OData plain entity sets.

12 plain entity sets. A single GET returns the whole set (verified: ~86k rows,
no nextLink) — a stateless full pull per set.
"""
from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import SLUG, _entity, _odata_all

EXPECTATIVAS_SETS = {
    "expectativas-expectativamercadomensais": "ExpectativaMercadoMensais",
    "expectativas-expectativamercadotop5trimestral": "ExpectativaMercadoTop5Trimestral",
    "expectativas-expectativasmercadoanuais": "ExpectativasMercadoAnuais",
    "expectativas-expectativasmercadoinflacao12meses": "ExpectativasMercadoInflacao12Meses",
    "expectativas-expectativasmercadoinflacao24meses": "ExpectativasMercadoInflacao24Meses",
    "expectativas-expectativasmercadoselic": "ExpectativasMercadoSelic",
    "expectativas-expectativasmercadotop5anuais": "ExpectativasMercadoTop5Anuais",
    "expectativas-expectativasmercadotop5inflacao12meses": "ExpectativasMercadoTop5Inflacao12Meses",
    "expectativas-expectativasmercadotop5inflacao24meses": "ExpectativasMercadoTop5Inflacao24Meses",
    "expectativas-expectativasmercadotop5mensais": "ExpectativasMercadoTop5Mensais",
    "expectativas-expectativasmercadotop5selic": "ExpectativasMercadoTop5Selic",
    "expectativas-expectativasmercadotrimestrais": "ExpectativasMercadoTrimestrais",
}


def fetch_expectativas(node_id: str) -> None:
    """Stateless full pull of one plain Expectativas (Focus) entity set."""
    resource = EXPECTATIVAS_SETS[_entity(node_id)]
    rows = _odata_all("Expectativas", resource, {})
    save_raw_ndjson(rows, node_id)


def _expectativas_sql(dep: str) -> str:
    # Every Focus set carries a string `Data` observation date; retype it, pass
    # the rest of the relational columns through untouched.
    return f'SELECT * EXCLUDE (Data), TRY_CAST(Data AS DATE) AS Data FROM "{dep}"'


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{e}", fn=fetch_expectativas, kind="download")
    for e in EXPECTATIVAS_SETS
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-{e}-transform",
        deps=[f"{SLUG}-{e}"],
        sql=_expectativas_sql(f"{SLUG}-{e}"),
    )
    for e in EXPECTATIVAS_SETS
]
