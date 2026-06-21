"""IFDATA (financial institutions) — Olinda OData parameterized FunctionImports.

Two FunctionImports keyed by reporting period (AnoMes), backfilled as an
AnoMes-bucketed firehose:
  - IfDataCadastro is keyed by AnoMes only.
  - IfDataValores by AnoMes × TipoInstituicao × Relatorio (reports enumerated
    from ListaDeRelatorio).
"""
from datetime import date, datetime, timezone
import re

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    list_raw_files,
    save_raw_ndjson,
    save_state,
)

from utils import (
    OLINDA,
    SLUG,
    STATE_VERSION,
    _entity,
    _env_int,
    _fetch_json,
    _odata_function,
    _skip_reason,
)

IFDATA_START_YEAR = _env_int("BCB_IFDATA_START_YEAR", 2000)

# IFData enumeration knobs.
IFDATA_TIPOS = (1, 2, 3, 4)      # TipoInstituicao buckets (prudential / financial / ...)

_ANOMES_RE = re.compile(r"-(\d{6})\.ndjson\.zst$")


def _quarters(start_year: int):
    """Yield AnoMes ints (YYYYMM) at quarter-ends from start_year to this quarter."""
    today = datetime.now(tz=timezone.utc).date()
    for y in range(start_year, today.year + 1):
        for mm in (3, 6, 9, 12):
            anomes = y * 100 + mm
            if date(y, mm, 1) <= today:
                yield anomes


def fetch_ifdata(node_id: str) -> None:
    """AnoMes-bucketed firehose for an IFDATA function.

    IfDataCadastro is keyed by AnoMes only; IfDataValores by AnoMes ×
    TipoInstituicao × Relatorio (reports enumerated from ListaDeRelatorio).
    One raw batch per AnoMes, sweeping every quarter from the floor to now.

    Raw is run-scoped in this harness (runs/<run_id>/raw/...) while state is
    durable across runs, so the set of already-done quarters is derived from the
    raw present in THIS run's scope — never a globally-persisted watermark. A
    watermark would survive into a fresh run and make it skip every quarter, yet
    land its (empty) raw in a new scope, leaving the transform with no raw to
    read — exactly the failure that poisoned ifdatacadastro. Deriving the
    done-set from raw means a fresh run re-pulls the corpus while a continuation
    (same RUN_ID, shared raw scope) resumes from the quarter it left off. State
    is still written, but only as an observable record — never load-bearing.
    """
    entity = _entity(node_id)

    # Authoritative done-set: AnoMes buckets already written in this run's scope.
    done: set[int] = set()
    for rel in list_raw_files(f"{node_id}-*.ndjson.zst"):
        m = _ANOMES_RE.search(rel)
        if m:
            done.add(int(m.group(1)))

    relatorios: list[str] = []
    if entity == "ifdata-ifdatavalores":
        lista = _fetch_json(f"{OLINDA}/IFDATA/versao/v1/odata/ListaDeRelatorio()",
                            {"$format": "json"}).get("value", [])
        relatorios = [str(r["NumeroRelatorio"]) for r in lista if r.get("NumeroRelatorio")]

    for anomes in _quarters(IFDATA_START_YEAR):
        if anomes in done:
            continue
        rows: list[dict] = []
        if entity == "ifdata-ifdatacadastro":
            try:
                rows = _odata_function("IFDATA", "IfDataCadastro", {"AnoMes": anomes})
            except httpx.HTTPError as exc:
                print(f"skip {node_id} anomes={anomes}: {_skip_reason(exc)}")
        else:
            for tipo in IFDATA_TIPOS:
                for rel in relatorios:
                    try:
                        got = _odata_function(
                            "IFDATA", "IfDataValores",
                            {"AnoMes": anomes, "TipoInstituicao": tipo, "Relatorio": f"'{rel}'"},
                        )
                    except httpx.HTTPError as exc:
                        print(f"skip {node_id} anomes={anomes} tipo={tipo} rel={rel}: "
                              f"{_skip_reason(exc)}")
                        continue
                    rows.extend(got)
        if rows:
            save_raw_ndjson(rows, f"{node_id}-{anomes}")
            done.add(anomes)
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "completed": sorted(done),
            "last_success_at": datetime.now(tz=timezone.utc).isoformat(),
        })


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-ifdata-ifdatacadastro", fn=fetch_ifdata, kind="download"),
    NodeSpec(id=f"{SLUG}-ifdata-ifdatavalores", fn=fetch_ifdata, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{SLUG}-ifdata-ifdatacadastro-transform",
        deps=[f"{SLUG}-ifdata-ifdatacadastro"],
        sql=f'SELECT * FROM "{SLUG}-ifdata-ifdatacadastro"',
    ),
    SqlNodeSpec(
        id=f"{SLUG}-ifdata-ifdatavalores-transform",
        deps=[f"{SLUG}-ifdata-ifdatavalores"],
        sql=f'SELECT * FROM "{SLUG}-ifdata-ifdatavalores"',
    ),
]
