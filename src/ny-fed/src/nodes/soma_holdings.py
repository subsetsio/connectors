"""NY Fed — SOMA security-level holdings (latest as-of snapshot)."""

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import get_json, project

_HOLDING_FIELDS = (
    "asOfDate", "cusip", "securityType", "maturityDate", "issuer",
    "coupon", "spread", "parValue", "inflationCompensation",
    "percentOutstanding", "changeFromPriorWeek", "changeFromPriorYear",
)


def fetch_soma_holdings(node_id: str) -> None:
    # Latest as-of snapshot (security-level). The summary lists every as-of date.
    payload = get_json("soma/summary.json")
    summary = payload.get("soma", {}).get("summary", [])
    as_of = max(s["asOfDate"] for s in summary if s.get("asOfDate"))
    rows = []
    for group, path in (
        ("Treasury", f"soma/tsy/get/all/asof/{as_of}.json"),
        ("Agency", f"soma/agency/get/asof/{as_of}.json"),
    ):
        holdings = get_json(path).get("soma", {}).get("holdings", [])
        rows.extend(
            project(h, _HOLDING_FIELDS, extra={"instrumentGroup": group})
            for h in holdings
        )
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-soma-holdings", fn=fetch_soma_holdings, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-soma-holdings-transform",
        deps=["ny-fed-soma-holdings"],
        sql='''
            SELECT
                TRY_CAST(asOfDate AS DATE)           AS as_of_date,
                instrumentGroup                      AS instrument_group,
                securityType                         AS security_type,
                cusip,
                TRY_CAST(maturityDate AS DATE)       AS maturity_date,
                NULLIF(issuer, '')                   AS issuer,
                TRY_CAST(NULLIF(coupon, '') AS DOUBLE)   AS coupon_rate,
                TRY_CAST(NULLIF(parValue, '') AS DOUBLE) AS par_value,
                TRY_CAST(NULLIF(inflationCompensation, '') AS DOUBLE) AS inflation_compensation,
                TRY_CAST(NULLIF(percentOutstanding, '') AS DOUBLE)    AS percent_outstanding,
                TRY_CAST(NULLIF(changeFromPriorWeek, '') AS DOUBLE)   AS change_from_prior_week,
                TRY_CAST(NULLIF(changeFromPriorYear, '') AS DOUBLE)   AS change_from_prior_year
            FROM "ny-fed-soma-holdings"
            WHERE TRY_CAST(asOfDate AS DATE) IS NOT NULL AND cusip IS NOT NULL AND cusip <> ''
        ''',
    ),
]
