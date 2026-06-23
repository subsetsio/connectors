"""Federal Reserve Bank of New York — Markets Data APIs connector.

Single unauthenticated REST API at https://markets.newyorkfed.org. Each subset
maps to one endpoint family. Strategy is stateless full re-pull every run: the
whole corpus is small (a few hundred MB across all subsets) and fetches in a few
minutes, so there is no watermark/cursor state — revisions and late corrections
are picked up for free. Most operation/rate families accept a single wide
date-range query (startDate=2000-01-01..today); securities lending is the lone
exception (it caps the query window at ~1 year) so it is chunked by calendar
year from 1998 to the current year.
"""

import csv
import io
import json
import re
from datetime import datetime, timezone

import pyarrow as pa
from subsets_utils import (
    NodeSpec,
    SqlNodeSpec,
    get,
    save_raw_ndjson,
    save_raw_parquet,
    transient_retry,
)

BASE = "https://markets.newyorkfed.org"
START = "2000-01-01"  # safe early bound; all series begin well after this
SECLENDING_START_YEAR = 1998  # data exists from ~1999; earlier years return []


@transient_retry()
def _get(url, params=None):
    resp = get(url, params=params, timeout=(10.0, 180.0))
    resp.raise_for_status()
    return resp


def _today():
    return datetime.now(tz=timezone.utc).date().isoformat()


def _uniform(rows):
    """Reindex every record to the union of all keys (missing -> None) so the
    NDJSON has a stable, uniform column set regardless of per-record drift."""
    keys = []
    seen = set()
    for r in rows:
        for k in r:
            if k not in seen:
                seen.add(k)
                keys.append(k)
    return [{k: r.get(k) for k in keys} for r in rows]


def _csv_to_string_table(text, colnames):
    """Parse a CSV body into a pyarrow table where every column is a string.
    Typing/casting happens in the SQL transform."""
    reader = csv.reader(io.StringIO(text))
    next(reader, None)  # drop header row
    cols = [[] for _ in colnames]
    for row in reader:
        if not row:
            continue
        for i in range(len(colnames)):
            cols[i].append(row[i] if i < len(row) else None)
    schema = pa.schema([(n, pa.string()) for n in colnames])
    return pa.table({n: pa.array(cols[i], pa.string()) for i, n in enumerate(colnames)}, schema=schema)


# --- reference rates -------------------------------------------------------
def fetch_reference_rates(node_id):
    end = _today()
    rows = []
    for cls in ("secured", "unsecured"):
        d = _get(f"{BASE}/api/rates/{cls}/all/search.json", {"startDate": START, "endDate": end}).json()
        rows.extend(d.get("refRates", []))
    save_raw_ndjson(_uniform(rows), node_id)


# --- treasury securities operations ---------------------------------------
def fetch_treasury_operations(node_id):
    d = _get(f"{BASE}/api/tsy/all/results/summary/search.json", {"startDate": START, "endDate": _today()}).json()
    save_raw_ndjson(_uniform(d["treasury"]["auctions"]), node_id)


# --- agency MBS operations -------------------------------------------------
def fetch_agency_mbs_operations(node_id):
    d = _get(f"{BASE}/api/ambs/all/results/summary/search.json", {"startDate": START, "endDate": _today()}).json()
    save_raw_ndjson(_uniform(d["ambs"]["auctions"]), node_id)


# --- repo / reverse repo operations ---------------------------------------
def fetch_repo_operations(node_id):
    d = _get(f"{BASE}/api/rp/results/search.json", {"startDate": START, "endDate": _today()}).json()
    ops = d["repo"]["operations"]
    # Drop the nested per-collateral `details` and counterparty `propositions`
    # arrays to keep one flat row per operation.
    rows = [{k: v for k, v in o.items() if k not in ("details", "propositions")} for o in ops]
    save_raw_ndjson(_uniform(rows), node_id)


# --- securities lending operations (year-chunked: ~1yr window cap) --------
def fetch_securities_lending_operations(node_id):
    rows = []
    current_year = datetime.now(tz=timezone.utc).year
    for year in range(SECLENDING_START_YEAR, current_year + 1):
        d = _get(
            f"{BASE}/api/seclending/all/results/summary/search.json",
            {"startDate": f"{year}-01-01", "endDate": f"{year}-12-31"},
        ).json()
        rows.extend(d["seclending"]["operations"])
    save_raw_ndjson(_uniform(rows), node_id)


# --- central bank FX (liquidity) swaps ------------------------------------
def fetch_central_bank_fx_swaps(node_id):
    d = _get(f"{BASE}/api/fxs/all/search.json", {"startDate": START, "endDate": _today()}).json()
    save_raw_ndjson(_uniform(d["fxSwaps"]["operations"]), node_id)


# --- primary dealer time-series catalog -----------------------------------
def fetch_primary_dealer_series(node_id):
    d = _get(f"{BASE}/api/pd/list/timeseries.json").json()
    save_raw_ndjson(_uniform(d["pd"]["timeseries"]), node_id)


# --- primary dealer statistics values (bulk CSV) --------------------------
def fetch_primary_dealer_values(node_id):
    text = _get(f"{BASE}/api/pd/get/all/timeseries.csv").text
    table = _csv_to_string_table(text, ["as_of_date", "time_series", "value_millions"])
    save_raw_parquet(table, node_id)


# --- primary dealer market share (latest snapshot, qtrly + ytd) -----------
def fetch_primary_dealer_market_share(node_id):
    rows = []
    for period in ("qtrly", "ytd"):
        text = _get(f"{BASE}/api/marketshare/{period}/latest.json").text
        # Suppressed values are serialized as a bare `*`, which is invalid JSON.
        d = json.loads(re.sub(r":\s*\*", ": null", text))
        ms = d["pd"]["marketshare"]
        for grp in ms.values():
            if not isinstance(grp, dict):
                continue
            release = grp.get("releaseDate")
            title = grp.get("title")
            for category in ("interDealerBrokers", "others", "totals"):
                for item in grp.get(category, []):
                    row = dict(item)
                    row["period"] = period
                    row["category"] = category
                    row["releaseDate"] = release
                    row["title"] = title
                    rows.append(row)
    save_raw_ndjson(_uniform(rows), node_id)


# --- SOMA holdings weekly summary -----------------------------------------
def fetch_soma_summary(node_id):
    d = _get(f"{BASE}/api/soma/summary.json").json()
    save_raw_ndjson(_uniform(d["soma"]["summary"]), node_id)


# --- SOMA Treasury holdings detail by CUSIP (monthly bulk CSV) ------------
def fetch_soma_holdings(node_id):
    text = _get(f"{BASE}/api/soma/tsy/get/monthly.csv").text
    cols = [
        "as_of_date", "cusip", "security_type", "security_description", "term",
        "maturity_date", "issuer", "spread_pct", "coupon_pct", "current_face_value",
        "par_value", "inflation_compensation", "percent_outstanding",
        "change_from_prior_week", "change_from_prior_year", "is_aggregated",
    ]
    table = _csv_to_string_table(text, cols)
    save_raw_parquet(table, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="federal-reserve-bank-of-new-york-reference-rates", fn=fetch_reference_rates, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-treasury-operations", fn=fetch_treasury_operations, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-agency-mbs-operations", fn=fetch_agency_mbs_operations, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-repo-operations", fn=fetch_repo_operations, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-securities-lending-operations", fn=fetch_securities_lending_operations, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-central-bank-fx-swaps", fn=fetch_central_bank_fx_swaps, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-primary-dealer-series", fn=fetch_primary_dealer_series, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-primary-dealer-values", fn=fetch_primary_dealer_values, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-primary-dealer-market-share", fn=fetch_primary_dealer_market_share, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-soma-summary", fn=fetch_soma_summary, kind="download"),
    NodeSpec(id="federal-reserve-bank-of-new-york-soma-holdings", fn=fetch_soma_holdings, kind="download"),
]


TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-reference-rates-transform",
        deps=["federal-reserve-bank-of-new-york-reference-rates"],
        sql='''
            SELECT
                CAST(effectiveDate AS DATE)            AS effective_date,
                type                                   AS rate_type,
                TRY_CAST(percentRate AS DOUBLE)        AS percent_rate,
                TRY_CAST(percentPercentile1 AS DOUBLE) AS percentile_1,
                TRY_CAST(percentPercentile25 AS DOUBLE) AS percentile_25,
                TRY_CAST(percentPercentile75 AS DOUBLE) AS percentile_75,
                TRY_CAST(percentPercentile99 AS DOUBLE) AS percentile_99,
                TRY_CAST(volumeInBillions AS DOUBLE)   AS volume_billions,
                TRY_CAST(targetRateFrom AS DOUBLE)     AS target_rate_from,
                TRY_CAST(targetRateTo AS DOUBLE)       AS target_rate_to,
                TRY_CAST(average30day AS DOUBLE)       AS average_30day,
                TRY_CAST(average90day AS DOUBLE)       AS average_90day,
                TRY_CAST(average180day AS DOUBLE)      AS average_180day,
                TRY_CAST("index" AS DOUBLE)            AS sofr_index
            FROM "federal-reserve-bank-of-new-york-reference-rates"
            WHERE effectiveDate IS NOT NULL AND type IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-treasury-operations-transform",
        deps=["federal-reserve-bank-of-new-york-treasury-operations"],
        sql='''
            SELECT
                operationId                            AS operation_id,
                CAST(operationDate AS DATE)            AS operation_date,
                TRY_CAST(settlementDate AS DATE)       AS settlement_date,
                operationType                          AS operation_type,
                operationDirection                     AS operation_direction,
                auctionMethod                          AS auction_method,
                auctionStatus                          AS auction_status,
                TRY_CAST(maturityRangeStart AS DATE)   AS maturity_range_start,
                TRY_CAST(maturityRangeEnd AS DATE)     AS maturity_range_end,
                TRY_CAST(totalParAmtSubmitted AS DOUBLE) AS total_par_submitted,
                TRY_CAST(totalParAmtAccepted AS DOUBLE)  AS total_par_accepted,
                CAST(releaseTime AS VARCHAR)           AS release_time,
                CAST(closeTime AS VARCHAR)             AS close_time,
                note,
                TRY_CAST(lastUpdated AS TIMESTAMP)     AS last_updated
            FROM "federal-reserve-bank-of-new-york-treasury-operations"
            WHERE operationId IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-agency-mbs-operations-transform",
        deps=["federal-reserve-bank-of-new-york-agency-mbs-operations"],
        sql='''
            SELECT
                operationId                            AS operation_id,
                CAST(operationDate AS DATE)            AS operation_date,
                TRY_CAST(settlementDate AS DATE)       AS settlement_date,
                operationType                          AS operation_type,
                operationDirection                     AS operation_direction,
                method                                 AS method,
                auctionStatus                          AS auction_status,
                classType                              AS class_type,
                TRY_CAST(totalAmtSubmittedPar AS DOUBLE) AS total_submitted_par,
                TRY_CAST(totalAmtAcceptedPar AS DOUBLE)  AS total_accepted_par,
                TRY_CAST(totalSubmittedCurrFace AS DOUBLE) AS total_submitted_curr_face,
                TRY_CAST(totalAcceptedCurrFace AS DOUBLE)  AS total_accepted_curr_face,
                note,
                TRY_CAST(lastUpdated AS TIMESTAMP)     AS last_updated
            FROM "federal-reserve-bank-of-new-york-agency-mbs-operations"
            WHERE operationId IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-repo-operations-transform",
        deps=["federal-reserve-bank-of-new-york-repo-operations"],
        sql='''
            SELECT
                operationId                            AS operation_id,
                CAST(operationDate AS DATE)            AS operation_date,
                TRY_CAST(settlementDate AS DATE)       AS settlement_date,
                TRY_CAST(maturityDate AS DATE)         AS maturity_date,
                operationType                          AS operation_type,
                operationMethod                        AS operation_method,
                settlementType                         AS settlement_type,
                term                                   AS term,
                TRY_CAST(termCalenderDays AS INTEGER)  AS term_calendar_days,
                auctionStatus                          AS auction_status,
                TRY_CAST(participatingCpty AS INTEGER) AS participating_cpty,
                TRY_CAST(acceptedCpty AS INTEGER)      AS accepted_cpty,
                TRY_CAST(totalAmtSubmitted AS DOUBLE)  AS total_amt_submitted,
                TRY_CAST(totalAmtAccepted AS DOUBLE)   AS total_amt_accepted,
                TRY_CAST(lastUpdated AS TIMESTAMP)     AS last_updated
            FROM "federal-reserve-bank-of-new-york-repo-operations"
            WHERE operationId IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-securities-lending-operations-transform",
        deps=["federal-reserve-bank-of-new-york-securities-lending-operations"],
        sql='''
            SELECT
                operationId                            AS operation_id,
                CAST(operationDate AS DATE)            AS operation_date,
                TRY_CAST(settlementDate AS DATE)       AS settlement_date,
                TRY_CAST(maturityDate AS DATE)         AS maturity_date,
                operationType                          AS operation_type,
                auctionStatus                          AS auction_status,
                CAST(releaseTime AS VARCHAR)           AS release_time,
                CAST(closeTime AS VARCHAR)             AS close_time,
                TRY_CAST(totalParAmtSubmitted AS DOUBLE) AS total_par_submitted,
                TRY_CAST(totalParAmtAccepted AS DOUBLE)  AS total_par_accepted,
                note,
                TRY_CAST(lastUpdated AS TIMESTAMP)     AS last_updated
            FROM "federal-reserve-bank-of-new-york-securities-lending-operations"
            WHERE operationId IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-central-bank-fx-swaps-transform",
        deps=["federal-reserve-bank-of-new-york-central-bank-fx-swaps"],
        sql='''
            SELECT
                operationType                          AS operation_type,
                counterparty,
                currency,
                CAST(tradeDate AS DATE)                AS trade_date,
                TRY_CAST(settlementDate AS DATE)       AS settlement_date,
                TRY_CAST(maturityDate AS DATE)         AS maturity_date,
                TRY_CAST(termInDays AS INTEGER)        AS term_in_days,
                TRY_CAST(amount AS DOUBLE)             AS amount,
                TRY_CAST(interestRate AS DOUBLE)       AS interest_rate,
                TRY_CAST(lastUpdated AS TIMESTAMP)     AS last_updated
            FROM "federal-reserve-bank-of-new-york-central-bank-fx-swaps"
            WHERE tradeDate IS NOT NULL AND counterparty IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-primary-dealer-series-transform",
        deps=["federal-reserve-bank-of-new-york-primary-dealer-series"],
        sql='''
            SELECT
                keyid       AS key_id,
                description,
                seriesbreak AS series_break
            FROM "federal-reserve-bank-of-new-york-primary-dealer-series"
            WHERE keyid IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-primary-dealer-values-transform",
        deps=["federal-reserve-bank-of-new-york-primary-dealer-values"],
        sql='''
            SELECT
                CAST(as_of_date AS DATE)         AS as_of_date,
                time_series                      AS key_id,
                TRY_CAST(value_millions AS DOUBLE) AS value_millions
            FROM "federal-reserve-bank-of-new-york-primary-dealer-values"
            WHERE as_of_date IS NOT NULL
              AND time_series IS NOT NULL
              AND TRY_CAST(value_millions AS DOUBLE) IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-primary-dealer-market-share-transform",
        deps=["federal-reserve-bank-of-new-york-primary-dealer-market-share"],
        sql='''
            SELECT
                period,
                category,
                CAST(releaseDate AS DATE)              AS release_date,
                title,
                securityType                           AS security_type,
                security,
                percentFirstQuintRange                 AS first_quint_range,
                TRY_CAST(percentFirstQuintMktShare AS DOUBLE)  AS first_quint_mkt_share,
                percentSecondQuintRange                AS second_quint_range,
                TRY_CAST(percentSecondQuintMktShare AS DOUBLE) AS second_quint_mkt_share,
                percentThirdQuintRange                 AS third_quint_range,
                TRY_CAST(percentThirdQuintMktShare AS DOUBLE)  AS third_quint_mkt_share,
                percentFourthQuintRange                AS fourth_quint_range,
                TRY_CAST(percentFourthQuintMktShare AS DOUBLE) AS fourth_quint_mkt_share,
                percentFifthQuintRange                 AS fifth_quint_range,
                TRY_CAST(percentFifthQuintMktShare AS DOUBLE)  AS fifth_quint_mkt_share,
                TRY_CAST(dailyAvgVolInMillions AS DOUBLE)      AS daily_avg_vol_millions
            FROM "federal-reserve-bank-of-new-york-primary-dealer-market-share"
            WHERE period IS NOT NULL AND security IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-soma-summary-transform",
        deps=["federal-reserve-bank-of-new-york-soma-summary"],
        sql='''
            SELECT
                CAST(asOfDate AS DATE)                 AS as_of_date,
                TRY_CAST(bills AS DOUBLE)              AS bills,
                TRY_CAST(notesbonds AS DOUBLE)         AS notes_bonds,
                TRY_CAST(tips AS DOUBLE)               AS tips,
                TRY_CAST(tipsInflationCompensation AS DOUBLE) AS tips_inflation_compensation,
                TRY_CAST(frn AS DOUBLE)                AS frn,
                TRY_CAST(mbs AS DOUBLE)                AS mbs,
                TRY_CAST(cmbs AS DOUBLE)               AS cmbs,
                TRY_CAST(agencies AS DOUBLE)           AS agencies,
                TRY_CAST(total AS DOUBLE)              AS total
            FROM "federal-reserve-bank-of-new-york-soma-summary"
            WHERE asOfDate IS NOT NULL
        ''',
    ),
    SqlNodeSpec(
        id="federal-reserve-bank-of-new-york-soma-holdings-transform",
        deps=["federal-reserve-bank-of-new-york-soma-holdings"],
        sql='''
            SELECT
                CAST(as_of_date AS DATE)               AS as_of_date,
                TRIM(cusip, chr(39)) AS cusip,
                security_type,
                security_description,
                term,
                TRY_CAST(maturity_date AS DATE)        AS maturity_date,
                issuer,
                TRY_CAST(spread_pct AS DOUBLE)         AS spread_pct,
                TRY_CAST(coupon_pct AS DOUBLE)         AS coupon_pct,
                TRY_CAST(current_face_value AS DOUBLE) AS current_face_value,
                TRY_CAST(par_value AS DOUBLE)          AS par_value,
                TRY_CAST(inflation_compensation AS DOUBLE) AS inflation_compensation,
                TRY_CAST(percent_outstanding AS DOUBLE) AS percent_outstanding,
                is_aggregated
            FROM "federal-reserve-bank-of-new-york-soma-holdings"
            WHERE as_of_date IS NOT NULL
        ''',
    ),
]
