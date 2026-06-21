"""PTAX (FX bulletins) — Olinda OData *Periodo* FunctionImports.

Two *Periodo* FunctionImports — CotacaoDolarPeriodo (USD) and CotacaoMoedaPeriodo
(per currency). Each takes a date range and returns the full daily bulletin
history; we sweep one call per year.

Not built (gated at rank): the PTAX *Dia* (single-date) functions and the two
`codigoMoeda`-keyed functions. The *Dia* functions are exact duplicates of the
*Periodo* series (identical schema; Periodo already returns the full daily
history) and are structurally infeasible to backfill one HTTP call per calendar
day since 1999. The `codigoMoeda`-keyed functions return HTTP 500 for every code
probed (verified 2026-06), so they can only ever publish empty tables.
"""
from datetime import datetime, timezone

import httpx

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson

from utils import (
    SLUG,
    _entity,
    _env_int,
    _odata_all,
    _odata_function,
    _skip_reason,
)

# Backfill floor (moving ceiling = today).
PTAX_START_YEAR = _env_int("BCB_PTAX_START_YEAR", 1999)   # Real-plan era; earliest meaningful FX history

# PTAX period functions: (function name, ordered date param names, currency-keyed?)
PTAX_PERIOD = {
    "ptax-cotacaodolarperiodo": ("CotacaoDolarPeriodo", ("dataInicial", "dataFinalCotacao"), None),
    "ptax-cotacaomoedaperiodo": ("CotacaoMoedaPeriodo", ("dataInicial", "dataFinalCotacao"), "moeda"),
}


def _ptax_currencies() -> list[str]:
    """Currency symbols quoted from PTAX/Moedas (used for the symbol-keyed funcs)."""
    rows = _odata_all("PTAX", "Moedas", {})
    return [r["simbolo"] for r in rows if r.get("simbolo")]


def fetch_ptax_period(node_id: str) -> None:
    """Stateless full pull of a PTAX *Periodo* function, chunked one call/year.

    USD-only functions fetch once per year; currency-keyed functions fetch once
    per (currency, year). A failing sub-request (e.g. BCB's 500-ing codigoMoeda
    functions) is skipped so the rest of the corpus still lands.
    """
    entity = _entity(node_id)
    func, (p_lo, p_hi), ccy_key = PTAX_PERIOD[entity]
    this_year = datetime.now(tz=timezone.utc).year
    currencies = _ptax_currencies() if ccy_key else [None]

    out: list[dict] = []
    for ccy in currencies:
        for year in range(PTAX_START_YEAR, this_year + 1):
            args = {
                p_lo: f"'01-01-{year}'",
                p_hi: f"'12-31-{year}'",
            }
            if ccy_key:
                args = {ccy_key: f"'{ccy}'", **args}
            try:
                rows = _odata_function("PTAX", func, args)
            except httpx.HTTPError as exc:
                print(f"skip {node_id} ccy={ccy} year={year}: {_skip_reason(exc)}")
                continue
            for r in rows:
                if ccy_key:
                    r[ccy_key] = ccy
                out.append(r)
    save_raw_ndjson(out, node_id)


def _ptax_sql(dep: str) -> str:
    # Every PTAX bulletin carries a `dataHoraCotacao` timestamp string.
    return f'SELECT * EXCLUDE (dataHoraCotacao), TRY_CAST(dataHoraCotacao AS TIMESTAMP) AS dataHoraCotacao FROM "{dep}"'


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-{e}", fn=fetch_ptax_period, kind="download")
    for e in PTAX_PERIOD
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-{e}-transform",
        deps=[f"{SLUG}-{e}"],
        sql=_ptax_sql(f"{SLUG}-{e}"),
    )
    for e in PTAX_PERIOD
]
