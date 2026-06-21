"""NY Fed — agency MBS operations (parent op + flattened details)."""

from datetime import date

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import flatten_operations, search

_AMBS_PARENT = (
    "operationId", "operationDate", "operationType", "operationDirection",
    "method", "classType", "settlementDate",
    "totalAmtSubmittedPar", "totalAmtAcceptedPar",
)
_AMBS_DETAIL = ("securityDescription", "amtAcceptedPar", "inclusionExclusionFlag")


def fetch_ambs_operations(node_id: str) -> None:
    ops = search("ambs/all/results/details/search.json?startDate={startDate}&endDate={endDate}",
                 "ambs", "auctions", start=date(2013, 1, 1))
    rows = list(flatten_operations(ops, _AMBS_PARENT, _AMBS_DETAIL))
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-ambs-operations", fn=fetch_ambs_operations, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-ambs-operations-transform",
        deps=["ny-fed-ambs-operations"],
        sql='''
            SELECT
                TRY_CAST(operationDate AS DATE)      AS operation_date,
                operationId                          AS operation_id,
                operationType                        AS operation_type,
                operationDirection                   AS operation_direction,
                TRY_CAST(settlementDate AS DATE)     AS settlement_date,
                classType                            AS class_type,
                method,
                securityDescription                  AS security_description,
                inclusionExclusionFlag               AS inclusion_flag,
                TRY_CAST(totalAmtSubmittedPar AS DOUBLE) AS amount_submitted_par,
                TRY_CAST(amtAcceptedPar AS DOUBLE)       AS amount_accepted_par,
                TRY_CAST(totalAmtAcceptedPar AS DOUBLE)  AS total_amount_accepted_par
            FROM "ny-fed-ambs-operations"
            WHERE TRY_CAST(operationDate AS DATE) IS NOT NULL AND operationId IS NOT NULL
        ''',
    ),
]
