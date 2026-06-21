"""NY Fed — Treasury securities operations (parent op + flattened details)."""

from datetime import date

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import flatten_operations, search

_TSY_PARENT = (
    "operationId", "operationDate", "operationType", "operationDirection",
    "settlementDate", "maturityRangeStart", "maturityRangeEnd",
    "auctionMethod", "totalParAmtSubmitted", "totalParAmtAccepted",
)
_TSY_DETAIL = (
    "cusip", "securityDescription", "parAmountAccepted",
    "weightedAvgAccptPrice", "leastFavoriteAccptPrice",
)


def fetch_treasury_operations(node_id: str) -> None:
    ops = search("tsy/all/results/details/search.json?startDate={startDate}&endDate={endDate}",
                 "treasury", "auctions", start=date(2009, 1, 1))
    rows = list(flatten_operations(ops, _TSY_PARENT, _TSY_DETAIL))
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-treasury-operations", fn=fetch_treasury_operations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-treasury-operations-transform",
        deps=["ny-fed-treasury-operations"],
        sql='''
            SELECT
                TRY_CAST(operationDate AS DATE)      AS operation_date,
                operationId                          AS operation_id,
                operationType                        AS operation_type,
                operationDirection                   AS operation_direction,
                TRY_CAST(settlementDate AS DATE)     AS settlement_date,
                cusip,
                securityDescription                  AS security_description,
                TRY_CAST(maturityRangeStart AS DATE) AS maturity_range_start,
                TRY_CAST(maturityRangeEnd AS DATE)   AS maturity_range_end,
                auctionMethod                        AS auction_method,
                TRY_CAST(totalParAmtSubmitted AS DOUBLE) AS par_amount_submitted,
                TRY_CAST(parAmountAccepted AS DOUBLE)    AS par_amount_accepted,
                TRY_CAST(weightedAvgAccptPrice AS DOUBLE)   AS weighted_avg_price,
                TRY_CAST(leastFavoriteAccptPrice AS DOUBLE) AS least_favorable_price
            FROM "ny-fed-treasury-operations"
            WHERE TRY_CAST(operationDate AS DATE) IS NOT NULL AND operationId IS NOT NULL
        ''',
    ),
]
