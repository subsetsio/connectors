"""Czech National Bank — public financial-market REST API (api.cnb.cz/cnbapi).

Mechanism: 'rest' (no auth). Each family has a year-keyed bulk endpoint that
returns every record for a year in one JSON document, EXCEPT 'forward', which
has no year endpoint but offers a per-(currency-pair, maturity) date-range
endpoint that returns full history in one call.

Fetch shape: stateless full re-pull (shape 1). The whole corpus is a few
hundred-thousand rows total and re-fetchable in minutes; we never store a
watermark, so source revisions are picked up for free. Year coverage is
discovered, not hardcoded: we walk from a safe floor (CNB series do not predate
1990) up to the current year and skip any year whose endpoint returns no rows.

Raw is written as NDJSON per family: schemas differ across families, several
columns are nullable (pribid, nominalValue...), and 'omo' carries Czech-text
categorical fields — NDJSON is the forgiving choice; the SQL transform is the
type/correctness gate.
"""

import datetime

from subsets_utils import (
    NodeSpec,
    get,
    save_raw_ndjson,
)

BASE = "https://api.cnb.cz/cnbapi/"
FLOOR_YEAR = 1990  # safe lower bound; CNB API series do not predate this
SKD_FLOOR_YEAR = 2000  # /skd/daily has no year endpoint; older probes return empty

# entity_id -> (endpoint path template with {year}, response wrapper key, send lang=EN)
YEAR_FAMILIES = {
    "exrates-daily": ("exrates/daily-year", "rates", True),
    "exrates-monthly-averages": ("exrates/monthly-averages-year", "averages", True),
    "exrates-monthly-cumulative-averages": ("exrates/monthly-cumulative-averages-year", "averages", True),
    "exrates-quarterly-averages": ("exrates/quarterly-averages-year", "averages", True),
    "fxrates-daily": ("fxrates/daily-year", "rates", True),
    "pribor-daily": ("pribor/daily-year", "pribs", False),
    "czeonia-daily": ("czeonia/daily-year", "rates", False),
    "omo-daily": ("omo/daily-year", "operations", False),
}


def _get_json(path: str, params: dict) -> dict:
    resp = get(BASE + path, params=params, timeout=(10.0, 120.0))
    resp.raise_for_status()
    return resp.json()


def _entity_of(node_id: str) -> str:
    return node_id[len("czech-national-bank-"):]


def fetch_year_bulk(node_id: str) -> None:
    """Per-year bulk fetch for families exposing a `*-year` endpoint.

    Walks every year from FLOOR_YEAR to the current year; the endpoints return
    HTTP 200 with an empty array for years outside a family's coverage, so we
    simply skip empty years rather than hardcoding per-family start years.
    """
    asset = node_id
    entity = _entity_of(node_id)
    path, wrapper, want_lang = YEAR_FAMILIES[entity]
    current_year = datetime.date.today().year

    rows: list[dict] = []
    for year in range(FLOOR_YEAR, current_year + 1):
        params: dict = {"year": year}
        if want_lang:
            params["lang"] = "EN"
        payload = _get_json(path, params)
        chunk = payload.get(wrapper) or []
        rows.extend(chunk)

    save_raw_ndjson(rows, asset)


def fetch_skd(node_id: str) -> None:
    """SKD short-term bond settlements.

    The OpenAPI spec exposes only /skd/daily?date=YYYY-MM-DD, not a year/range
    endpoint. Weekend and holiday requests repeat the previous valid settlement
    date, so we probe weekdays and deduplicate on the actual row identity.
    """
    asset = node_id
    current = datetime.date.today()
    day = datetime.date(SKD_FLOOR_YEAR, 1, 1)
    rows_by_key: dict[tuple, dict] = {}

    while day <= current:
        if day.weekday() < 5:
            payload = _get_json("skd/daily", {"date": day.isoformat()})
            for row in payload.get("skds") or []:
                key = (
                    row.get("settlementDate"),
                    row.get("isin"),
                    row.get("issueCode"),
                    row.get("nominalValueCZK"),
                )
                rows_by_key[key] = row
        day += datetime.timedelta(days=1)

    if not rows_by_key:
        raise RuntimeError("skd/daily returned no rows")

    rows = sorted(
        rows_by_key.values(),
        key=lambda r: (
            r.get("settlementDate") or "",
            r.get("isin") or "",
            r.get("issueCode") or "",
        ),
    )
    save_raw_ndjson(rows, asset)


def fetch_forward(node_id: str) -> None:
    """FX forward points: no year endpoint. Discover the live set of
    (currencyPair, maturity) combinations from the latest daily snapshot, then
    pull each combination's full history in one date-range call."""
    asset = node_id
    today = datetime.date.today().isoformat()

    latest = _get_json("forward/daily", {"date": today}).get("forwardPoints") or []
    combos = sorted({(r["ccyPair"], r["maturity"]) for r in latest})
    if not combos:
        raise RuntimeError("forward/daily returned no combinations to enumerate")

    rows: list[dict] = []
    for ccy_pair, maturity in combos:
        payload = _get_json(
            "forward/daily-range-currency-pair-maturity",
            {
                "currencyPair": ccy_pair,
                "maturity": maturity,
                "dateFrom": f"{FLOOR_YEAR}-01-01",
                "dateTo": today,
            },
        )
        rows.extend(payload.get("forwardPoints") or [])

    save_raw_ndjson(rows, asset)


DOWNLOAD_SPECS = [
    NodeSpec(id=f"czech-national-bank-{eid}", fn=fetch_year_bulk, kind="download")
    for eid in YEAR_FAMILIES
] + [
    NodeSpec(id="czech-national-bank-forward-daily", fn=fetch_forward, kind="download"),
    NodeSpec(id="czech-national-bank-skd-daily", fn=fetch_skd, kind="download"),
]
