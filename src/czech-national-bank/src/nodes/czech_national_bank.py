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
    SqlNodeSpec,
    get,
    transient_retry,
    save_raw_ndjson,
)

BASE = "https://api.cnb.cz/cnbapi/"
FLOOR_YEAR = 1990  # safe lower bound; CNB API series do not predate this

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


@transient_retry()
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
]


# --- Transforms: one published Delta table per subset. Thin parse/cast/dedup;
# overlap-free here (stateless full pull) but DISTINCT guards accidental dupes. ---

# exrates/daily-year returns a compact record (no country/currency labels);
# fxrates/daily-year returns the full record with country + currency.
_EXRATES_SQL = '''
    SELECT DISTINCT
        CAST(validFor AS DATE)        AS date,
        currencyCode                  AS currency_code,
        CAST(amount AS INTEGER)       AS amount,
        CAST(rate AS DOUBLE)          AS rate
    FROM "{dep}"
    WHERE validFor IS NOT NULL AND rate IS NOT NULL
'''

_FXRATES_SQL = '''
    SELECT DISTINCT
        CAST(validFor AS DATE)        AS date,
        currencyCode                  AS currency_code,
        country,
        currency,
        CAST(amount AS INTEGER)       AS amount,
        CAST(rate AS DOUBLE)          AS rate
    FROM "{dep}"
    WHERE validFor IS NOT NULL AND rate IS NOT NULL
'''

_AVG_SQL = '''
    SELECT DISTINCT
        CAST(year AS INTEGER)         AS year,
        month                         AS period,
        currencyCode                  AS currency_code,
        CAST(amount AS INTEGER)       AS amount,
        CAST(average AS DOUBLE)       AS average
    FROM "{dep}"
    WHERE year IS NOT NULL AND average IS NOT NULL
'''

_SQL_BY_ENTITY = {
    "exrates-daily": _EXRATES_SQL,
    "fxrates-daily": _FXRATES_SQL,
    "exrates-monthly-averages": _AVG_SQL,
    "exrates-monthly-cumulative-averages": _AVG_SQL,
    "exrates-quarterly-averages": _AVG_SQL,
    "pribor-daily": '''
        SELECT DISTINCT
            CAST(validFor AS DATE)    AS date,
            period                    AS term,
            CAST(pribor AS DOUBLE)    AS rate
        FROM "{dep}"
        WHERE validFor IS NOT NULL AND pribor IS NOT NULL
    ''',
    "czeonia-daily": '''
        SELECT DISTINCT
            CAST(validFor AS DATE)         AS date,
            CAST(rate AS DOUBLE)           AS rate,
            CAST(volumeInCZKmio AS DOUBLE) AS volume_czk_mio
        FROM "{dep}"
        WHERE validFor IS NOT NULL AND rate IS NOT NULL
    ''',
    "omo-daily": '''
        SELECT DISTINCT
            CAST(tradeDate AS DATE)                    AS trade_date,
            CAST(settlementDate AS DATE)               AS settlement_date,
            CAST(maturityDate AS DATE)                 AS maturity_date,
            operationType                              AS operation_type,
            liquidityImpact                            AS liquidity_impact,
            CAST(marginalRateInPercent AS DOUBLE)      AS marginal_rate_pct,
            CAST(averageBidRateInPercent AS DOUBLE)    AS average_bid_rate_pct,
            CAST(averageAllotedRateInPercent AS DOUBLE) AS average_alloted_rate_pct,
            CAST(totalBidVolumeInCZKbln AS DOUBLE)     AS total_bid_volume_czk_bln,
            CAST(totalAllotedVolumeInCZKbln AS DOUBLE) AS total_alloted_volume_czk_bln,
            CAST(totalNumberOfBids AS INTEGER)         AS total_number_of_bids,
            CAST(totalNumberOfAllotedBids AS INTEGER)  AS total_number_of_alloted_bids,
            CAST(allotmentPercentage AS DOUBLE)        AS allotment_pct
        FROM "{dep}"
        WHERE tradeDate IS NOT NULL
    ''',
    "forward-daily": '''
        SELECT DISTINCT
            CAST(validFor AS DATE)         AS date,
            ccyPair                        AS currency_pair,
            maturity,
            CAST(forwardPoints AS DOUBLE)  AS forward_points
        FROM "{dep}"
        WHERE validFor IS NOT NULL AND forwardPoints IS NOT NULL
    ''',
}

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id=f"{s.id}-transform",
        deps=[s.id],
        sql=_SQL_BY_ENTITY[_entity_of(s.id)].format(dep=s.id),
    )
    for s in DOWNLOAD_SPECS
]
