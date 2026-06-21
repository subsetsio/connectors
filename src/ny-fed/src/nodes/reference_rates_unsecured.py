"""NY Fed — unsecured reference rates (EFFR, OBFR)."""

from datetime import date

from subsets_utils import NodeSpec, SqlNodeSpec, save_raw_ndjson
from utils import project, search

_RATE_FIELDS = (
    "effectiveDate", "type", "percentRate",
    "percentPercentile1", "percentPercentile25",
    "percentPercentile75", "percentPercentile99",
    "volumeInBillions", "targetRateFrom", "targetRateTo",
    "average30day", "average90day", "average180day", "index",
    "revisionIndicator",
)


def fetch_reference_rates_unsecured(node_id: str) -> None:
    rows = [
        project(r, _RATE_FIELDS)
        for r in search("rates/all/search.json?startDate={startDate}&endDate={endDate}",
                        "refRates", start=date(2016, 3, 1))
        if r.get("type") in ("EFFR", "OBFR")
    ]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-reference-rates-unsecured", fn=fetch_reference_rates_unsecured, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-reference-rates-unsecured-transform",
        deps=["ny-fed-reference-rates-unsecured"],
        sql='''
            SELECT DISTINCT
                TRY_CAST(effectiveDate AS DATE)      AS date,
                type                                 AS rate_type,
                TRY_CAST(percentRate AS DOUBLE)      AS rate_percent,
                TRY_CAST(percentPercentile1 AS DOUBLE)  AS percentile_1,
                TRY_CAST(percentPercentile25 AS DOUBLE) AS percentile_25,
                TRY_CAST(percentPercentile75 AS DOUBLE) AS percentile_75,
                TRY_CAST(percentPercentile99 AS DOUBLE) AS percentile_99,
                TRY_CAST(volumeInBillions AS DOUBLE) AS volume_billions,
                TRY_CAST(targetRateFrom AS DOUBLE)   AS target_rate_from,
                TRY_CAST(targetRateTo AS DOUBLE)     AS target_rate_to
            FROM "ny-fed-reference-rates-unsecured"
            WHERE TRY_CAST(effectiveDate AS DATE) IS NOT NULL AND type IS NOT NULL
        ''',
    ),
]
