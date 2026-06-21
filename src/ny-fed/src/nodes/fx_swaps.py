"""NY Fed — central bank liquidity swaps (FX swaps)."""

from datetime import date

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import project, search

_FXS_FIELDS = (
    "tradeDate", "settlementDate", "maturityDate", "operationType",
    "counterparty", "currency", "termInDays", "amount", "interestRate",
    "isSmallValue", "lastUpdated",
)


def fetch_fx_swaps(node_id: str) -> None:
    rows = [
        project(r, _FXS_FIELDS)
        for r in search("fxs/all/search.json?startDate={startDate}&endDate={endDate}",
                        "fxSwaps", "operations", start=date(2020, 1, 1))
    ]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-fx-swaps", fn=fetch_fx_swaps, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-fx-swaps-transform",
        deps=["ny-fed-fx-swaps"],
        sql='''
            SELECT DISTINCT
                TRY_CAST(tradeDate AS DATE)          AS trade_date,
                TRY_CAST(settlementDate AS DATE)     AS settlement_date,
                TRY_CAST(maturityDate AS DATE)       AS maturity_date,
                operationType                        AS operation_type,
                counterparty,
                currency,
                TRY_CAST(termInDays AS INTEGER)      AS term_days,
                TRY_CAST(amount AS DOUBLE)           AS amount,
                TRY_CAST(interestRate AS DOUBLE)     AS interest_rate
            FROM "ny-fed-fx-swaps"
            WHERE TRY_CAST(tradeDate AS DATE) IS NOT NULL AND currency IS NOT NULL
        ''',
    ),
]
