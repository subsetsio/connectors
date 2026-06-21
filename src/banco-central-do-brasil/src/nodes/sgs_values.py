"""SGS values — every series' full history via the SGS REST surface.

A code-bucketed firehose over https://api.bcb.gov.br/dados/serie. The set of
series codes is discovered from CKAN by `_discover_sgs_series`, imported from
`sgs_series` — that import is the explicit series→values dependency. Each run
(re)discovers the catalog and pulls every series' history; the relationship is
not buried in a separate copy of the discovery code.
"""
from datetime import datetime, timezone
import re

import httpx

from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    list_raw_files,
    save_raw_ndjson,
    save_state,
)

from utils import SLUG, STATE_VERSION, _env_int, _fetch_json, _skip_reason
from nodes.sgs_series import _discover_sgs_series

SGS_BASE = "https://api.bcb.gov.br/dados/serie"

# No per-run firehose budget: the fetch fn sweeps its whole range and writes one
# raw batch at a time, so the supervisor can interrupt the node at any point
# (→ pending → continuation) and the continuation resumes from the raw already
# written in this run's scope.
SGS_BATCH = _env_int("BCB_SGS_BATCH", 50)                 # series per raw batch file
SGS_START_YEAR = _env_int("BCB_SGS_START_YEAR", 1990)     # daily-history floor
SGS_WINDOW_YEARS = 10            # SGS rejects daily pulls wider than 10 years

_SGS_BATCH_RE = re.compile(r"-(\d{6})-(\d{6})\.ndjson\.zst$")


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
    # Resume index = highest code-index covered by raw already in this run.
    done_count = 0
    for rel in list_raw_files(f"{node_id}-*.ndjson.zst"):
        m = _SGS_BATCH_RE.search(rel)
        if m:
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
                save_raw_ndjson(batch, f"{node_id}-{batch_start:06d}-{done_count + processed:06d}")
                batch = []
                batch_start = done_count + processed
            _checkpoint(done_count + processed)
    if batch:
        save_raw_ndjson(batch, f"{node_id}-{batch_start:06d}-{done_count + processed:06d}")
    _checkpoint(done_count + processed)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"{SLUG}-sgs-values", fn=fetch_sgs_values, kind="download"),
]

TRANSFORM_SPECS = [
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
