"""Banco Central do Brasil — the connector's single node module.

Four BCB surfaces, one stateless-or-firehose fetch per subset, plus the thin
SQL transforms that publish each as a Delta table:

  - Expectativas (Focus survey)  — 12 Olinda OData plain entity sets; one GET
    returns the whole set (~tens of thousands of rows, no nextLink) → stateless
    full pull.
  - IFDATA (financial institutions) — 2 Olinda OData parameterized
    FunctionImports keyed by reporting period (AnoMes), backfilled as an
    AnoMes-bucketed firehose.
  - PTAX (FX bulletins) — 2 *Periodo* FunctionImports (USD and per-currency);
    each takes a date range and returns the full daily history → one call/year.
  - SGS (time series) — the series catalog discovered from the CKAN portal
    (sgs-series), and every series' full history via the SGS REST surface,
    pulled as a code-bucketed firehose (sgs-values).

Shared HTTP/retry/OData plumbing lives in `src/utils.py`; this module owns the
fetch logic, the DOWNLOAD_SPECS, and the TRANSFORM_SPECS.
"""
from datetime import date, datetime, timezone
import os
import re

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    list_raw_fragments,
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
    _odata_all,
    _odata_function,
    _skip_reason,
)

# ---------------------------------------------------------------------------
# Expectativas (Focus survey) — Olinda OData plain entity sets
# ---------------------------------------------------------------------------

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


# ---------------------------------------------------------------------------
# IFDATA (financial institutions) — Olinda OData FunctionImports (AnoMes firehose)
# ---------------------------------------------------------------------------

IFDATA_START_YEAR = _env_int("BCB_IFDATA_START_YEAR", 2000)

# IFData enumeration knobs.
IFDATA_TIPOS = (1, 2, 3, 4)      # TipoInstituicao buckets (prudential / financial / ...)



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

    The set of already-done quarters is derived from the raw manifest's
    fragments committed under THIS run's RUN_ID — never a globally-persisted
    watermark. A watermark would survive into a fresh run and make it skip
    every quarter yet commit no raw, leaving the transform with nothing to
    read — exactly the failure that poisoned ifdatacadastro. Deriving the
    done-set from committed fragments means a fresh run re-pulls the corpus
    while a continuation (same RUN_ID; each completed leg commits) resumes
    from the quarter it left off. State is still written, but only as an
    observable record — never load-bearing.
    """
    entity = _entity(node_id)

    # Authoritative done-set: AnoMes fragments COMMITTED in this run (the raw
    # manifest, never a directory listing — a failed leg's uncommitted buckets
    # must re-fetch or the manifest-first transform silently misses them).
    run_id = os.environ.get("RUN_ID", "unknown")
    done: set[int] = {
        int(frag) for frag, meta in list_raw_fragments(node_id, "ndjson.zst").items()
        if meta.get("run_id") == run_id and frag.isdigit()
    }

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
            save_raw_ndjson(rows, node_id, fragment=str(anomes))
            done.add(anomes)
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "completed": sorted(done),
            "last_success_at": datetime.now(tz=timezone.utc).isoformat(),
        })


# ---------------------------------------------------------------------------
# PTAX (FX bulletins) — Olinda OData *Periodo* FunctionImports
# ---------------------------------------------------------------------------
#
# Two *Periodo* FunctionImports — CotacaoDolarPeriodo (USD) and
# CotacaoMoedaPeriodo (per currency). Each takes a date range and returns the
# full daily bulletin history; we sweep one call per year.
#
# Not built (gated at rank): the PTAX *Dia* (single-date) functions and the two
# `codigoMoeda`-keyed functions. The *Dia* functions are exact duplicates of the
# *Periodo* series (identical schema; Periodo already returns the full daily
# history) and are structurally infeasible to backfill one HTTP call per calendar
# day since 1999. The `codigoMoeda`-keyed functions return HTTP 500 for every code
# probed (verified 2026-06), so they can only ever publish empty tables.

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


# ---------------------------------------------------------------------------
# SGS — series catalog (CKAN discovery) + every series' history (REST firehose)
# ---------------------------------------------------------------------------

CKAN = "https://dadosabertos.bcb.gov.br/api/3/action"
SGS_BASE = "https://api.bcb.gov.br/dados/serie"

_SGS_CODE_RE = re.compile(r"bcdata\.sgs\.(\d+)", re.I)

# No per-run firehose budget: the fetch fn sweeps its whole range and writes one
# raw batch at a time, so the supervisor can interrupt the node at any point
# (→ pending → continuation) and the continuation resumes from the raw already
# written in this run's scope.
SGS_BATCH = _env_int("BCB_SGS_BATCH", 50)                 # series per raw batch file
SGS_START_YEAR = _env_int("BCB_SGS_START_YEAR", 1990)     # daily-history floor
SGS_WINDOW_YEARS = 10            # SGS rejects daily pulls wider than 10 years



def _discover_sgs_series() -> list[dict]:
    """Enumerate SGS series from the CKAN portal.

    The SGS REST surface is a flat time-series API keyed by numeric series code;
    there is no native catalog, so the set of series is discovered from CKAN. A
    series is any package exposing a resource whose URL embeds
    `bcdata.sgs.<code>`. Returns sorted unique {code, name, title}.
    """
    found: dict[int, dict] = {}
    start = 0
    rows = 1000
    while True:
        res = _fetch_json(f"{CKAN}/package_search",
                          {"q": "sgs", "rows": rows, "start": start})["result"]
        results = res.get("results", [])
        if not results:
            break
        for p in results:
            for rsc in p.get("resources", []):
                m = _SGS_CODE_RE.search(rsc.get("url", "") or "")
                if m:
                    code = int(m.group(1))
                    found.setdefault(code, {
                        "code": code,
                        "name": p.get("name"),
                        "title": p.get("title"),
                    })
                    break
        start += len(results)
        if start >= res.get("count", 0):
            break
    return [found[c] for c in sorted(found)]


def fetch_sgs_series(node_id: str) -> None:
    """Stateless full pull of the SGS series catalog (one row per series)."""
    save_raw_ndjson(_discover_sgs_series(), node_id)


def _sgs_observations(code: int) -> list[dict]:
    """Full history of one SGS series, fetched in <=10-year windows.

    The SGS REST API rejects an unbounded pull of a *daily* series with HTTP 406
    ("janela de consulta de, no máximo, 10 anos"), so we always page by a fixed
    <=10-year window — which works for daily and monthly/annual series alike.
    A window that errors (HTTP 4xx, or a 200 HTML reject page for an invalid /
    decommissioned code, which fails JSON parsing) or returns a non-list body is
    skipped so one bad series can't sink the firehose.
    """
    today = datetime.now(tz=timezone.utc).date()
    out: list[dict] = []
    url = f"{SGS_BASE}/bcdata.sgs.{code}/dados"
    year = SGS_START_YEAR
    while year <= today.year:
        end = min(year + SGS_WINDOW_YEARS - 1, today.year)
        params = {"formato": "json", "dataInicial": f"01/01/{year}", "dataFinal": f"31/12/{end}"}
        try:
            obs = _fetch_json(url, params)
        except httpx.HTTPError as exc:
            print(f"skip sgs code={code} {year}-{end}: {_skip_reason(exc)}")
            obs = []
        except ValueError:
            # 200 with a non-JSON body — BCB's "Requisição inválida" reject page
            # for an invalid/dead code. Treat as no data and move on.
            print(f"skip sgs code={code} {year}-{end}: non-JSON body")
            obs = []
        if isinstance(obs, list):
            out.extend(o for o in obs if isinstance(o, dict))
        year += SGS_WINDOW_YEARS
    return out


def fetch_sgs_values(node_id: str) -> None:
    """Code-bucketed firehose: each SGS series' full history via SGS REST.

    Series codes are (re)discovered from CKAN each run and processed in sorted
    order, writing SGS_BATCH codes per raw batch file named with the
    [start, end) code-index span it covers.

    Raw is run-scoped while state is durable across runs, so the resume index is
    derived from the raw already written in THIS run's scope — never a
    globally-persisted watermark, which would survive into a fresh run and make
    it skip every code yet land no raw, leaving the transform empty. A fresh run
    re-pulls; a continuation (same RUN_ID) resumes after the highest code index
    already written. State is written only as an observable record.
    """
    # Resume index = highest code-index covered by fragments COMMITTED in this
    # run (fragment key: "<start>-<end>" span). The commit log, never a
    # directory listing — see the ifdata done-set note.
    run_id = os.environ.get("RUN_ID", "unknown")
    done_count = 0
    for frag, meta in list_raw_fragments(node_id, "ndjson.zst").items():
        m = re.fullmatch(r"(\d{6})-(\d{6})", frag)
        if m and meta.get("run_id") == run_id:
            done_count = max(done_count, int(m.group(2)))

    codes = [s["code"] for s in _discover_sgs_series()]
    todo = codes[done_count:]

    def _checkpoint(n: int) -> None:
        save_state(node_id, {
            "schema_version": STATE_VERSION,
            "completed": n,
            "last_success_at": datetime.now(tz=timezone.utc).isoformat(),
        })

    processed = 0
    batch: list[dict] = []
    batch_start = done_count
    for code in todo:
        obs = _sgs_observations(code)
        for o in obs:
            batch.append({"series_code": code, "data": o.get("data"), "valor": o.get("valor")})
        processed += 1
        if len(batch) >= 200000 or processed % SGS_BATCH == 0:
            if batch:
                save_raw_ndjson(batch, node_id,
                                fragment=f"{batch_start:06d}-{done_count + processed:06d}")
                batch = []
                batch_start = done_count + processed
            _checkpoint(done_count + processed)
    if batch:
        save_raw_ndjson(batch, f"{node_id}-{batch_start:06d}-{done_count + processed:06d}")
    _checkpoint(done_count + processed)


# ---------------------------------------------------------------------------
# Reference / dimension tables — plain Olinda sets and no-arg FunctionImports
# ---------------------------------------------------------------------------
#
# Small, un-parameterized surfaces: each is a single full pull. DatasReferencia
# (the Focus survey's per-indicator reference-date calendar) and Moedas (PTAX's
# currency dictionary) are plain entity sets; ListaDeRelatorio is a no-argument
# IFDATA FunctionImport (also consumed internally by fetch_ifdata).

REFERENCE_SETS = {
    "expectativas-datasreferencia": ("Expectativas", "DatasReferencia"),
    "ptax-moedas": ("PTAX", "Moedas"),
}


def fetch_reference_set(node_id: str) -> None:
    """Stateless full pull of a plain Olinda reference/dimension entity set."""
    service, resource = REFERENCE_SETS[_entity(node_id)]
    save_raw_ndjson(_odata_all(service, resource, {}), node_id)


def fetch_ifdata_relatorios(node_id: str) -> None:
    """Full pull of the IFDATA report catalog (ListaDeRelatorio, no params)."""
    rows = _fetch_json(f"{OLINDA}/IFDATA/versao/v1/odata/ListaDeRelatorio()",
                       {"$format": "json"}).get("value", [])
    save_raw_ndjson(rows, node_id)


# ---------------------------------------------------------------------------
# Specs — one download per entity-union member, one transform per subset
# ---------------------------------------------------------------------------
#
# Not built — excused via `waive-spec` (permanently unbuildable upstreams):
#   - ptax-cotacaomoedaperiodofechamento, ptax-cotacaomoedaaberturaouintermediario:
#     the two `codigoMoeda`-keyed PTAX FunctionImports return HTTP 500 for every
#     code (re-verified live 2026-07) — can only ever publish empty tables.
#   - ptax-cotacaodolardia, ptax-cotacaomoedadia: the *Dia* (single-date)
#     functions take no date range, so a full history is one HTTP call per
#     calendar day since 1999 (× ~150 currencies for MoedaDia ≈ 1M calls/run) —
#     disproportionate, and the closing-bulletin data duplicates the *Periodo*
#     series we already publish.

DOWNLOAD_SPECS = (
    [
        NodeSpec(id=f"{SLUG}-{e}", fn=fetch_expectativas, kind="download")
        for e in EXPECTATIVAS_SETS
    ]
    + [
        NodeSpec(id=f"{SLUG}-ifdata-ifdatacadastro", fn=fetch_ifdata, kind="download"),
        NodeSpec(id=f"{SLUG}-ifdata-ifdatavalores", fn=fetch_ifdata, kind="download"),
        NodeSpec(id=f"{SLUG}-ifdata-listaderelatorio", fn=fetch_ifdata_relatorios, kind="download"),
    ]
    + [
        NodeSpec(id=f"{SLUG}-{e}", fn=fetch_ptax_period, kind="download")
        for e in PTAX_PERIOD
    ]
    + [
        NodeSpec(id=f"{SLUG}-{e}", fn=fetch_reference_set, kind="download")
        for e in REFERENCE_SETS
    ]
    + [
        NodeSpec(id=f"{SLUG}-sgs-series", fn=fetch_sgs_series, kind="download"),
        NodeSpec(id=f"{SLUG}-sgs-values", fn=fetch_sgs_values, kind="download"),
    ]
)

TRANSFORM_SPECS = (
    [
        SqlNodeSpec(
            id=f"{SLUG}-{e}-transform",
            deps=[f"{SLUG}-{e}"],
            sql=_expectativas_sql(f"{SLUG}-{e}"),
        )
        for e in EXPECTATIVAS_SETS
    ]
    + [
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
    + [
        SqlNodeSpec(
            id=f"{SLUG}-{e}-transform",
            deps=[f"{SLUG}-{e}"],
            sql=_ptax_sql(f"{SLUG}-{e}"),
        )
        for e in PTAX_PERIOD
    ]
    + [
        SqlNodeSpec(
            id=f"{SLUG}-sgs-series-transform",
            deps=[f"{SLUG}-sgs-series"],
            sql=f'SELECT * FROM "{SLUG}-sgs-series"',
        ),
        SqlNodeSpec(
            id=f"{SLUG}-sgs-values-transform",
            deps=[f"{SLUG}-sgs-values"],
            sql=f'''
                SELECT
                    series_code,
                    CAST(strptime(data, '%d/%m/%Y') AS DATE) AS date,
                    TRY_CAST(valor AS DOUBLE)                AS value
                FROM "{SLUG}-sgs-values"
                WHERE valor IS NOT NULL AND valor <> ''
                ''',
        ),
    ]
)
