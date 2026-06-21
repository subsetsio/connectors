"""NY Fed — securities lending operations (parent op + flattened details)."""

from datetime import date

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import flatten_operations, search

_SECLEND_PARENT = (
    "operationId", "operationDate", "operationType",
    "settlementDate", "maturityDate",
)
_SECLEND_DETAIL = (
    "cusip", "securityDescription", "parAmtSubmitted", "parAmtAccepted",
    "weightedAverageRate", "somaHoldings", "theoAvailToBorrow",
    "actualAvailToBorrow", "outstandingLoans",
)


def fetch_securities_lending(node_id: str) -> None:
    ops = search("seclending/all/results/details/search.json?startDate={startDate}&endDate={endDate}",
                 "seclending", "operations", start=date(2008, 1, 1))
    rows = list(flatten_operations(ops, _SECLEND_PARENT, _SECLEND_DETAIL))
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-securities-lending", fn=fetch_securities_lending, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-securities-lending-transform",
        deps=["ny-fed-securities-lending"],
        sql='''
            SELECT
                TRY_CAST(operationDate AS DATE)      AS operation_date,
                operationId                          AS operation_id,
                TRY_CAST(settlementDate AS DATE)     AS settlement_date,
                TRY_CAST(maturityDate AS DATE)       AS maturity_date,
                cusip,
                securityDescription                  AS security_description,
                TRY_CAST(parAmtSubmitted AS DOUBLE)  AS par_amount_submitted,
                TRY_CAST(parAmtAccepted AS DOUBLE)   AS par_amount_accepted,
                TRY_CAST(weightedAverageRate AS DOUBLE) AS weighted_average_rate,
                TRY_CAST(somaHoldings AS DOUBLE)     AS soma_holdings,
                TRY_CAST(theoAvailToBorrow AS DOUBLE) AS theoretical_available,
                TRY_CAST(actualAvailToBorrow AS DOUBLE) AS actual_available,
                TRY_CAST(outstandingLoans AS DOUBLE) AS outstanding_loans
            FROM "ny-fed-securities-lending"
            WHERE TRY_CAST(operationDate AS DATE) IS NOT NULL AND cusip IS NOT NULL
        ''',
    ),
]
