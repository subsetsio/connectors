"""NY Fed — secured reference rates (SOFR, BGCR, TGCR, SOFRAI)."""

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


def fetch_reference_rates_secured(node_id: str) -> None:
    rows = [
        project(r, _RATE_FIELDS)
        for r in search("rates/secured/all/search.json?startDate={startDate}&endDate={endDate}",
                        "refRates", start=date(2018, 4, 2))
        if r.get("type") in ("SOFR", "BGCR", "TGCR", "SOFRAI")
    ]
    save_raw_ndjson(rows, node_id)


DOWNLOAD_SPECS = [
    NodeSpec(id="ny-fed-reference-rates-secured", fn=fetch_reference_rates_secured, kind="download"),
]

TRANSFORM_SPECS = [
    SqlNodeSpec(
        id="ny-fed-reference-rates-secured-transform",
        deps=["ny-fed-reference-rates-secured"],
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
                TRY_CAST(average30day AS DOUBLE)     AS average_30day,
                TRY_CAST(average90day AS DOUBLE)     AS average_90day,
                TRY_CAST(average180day AS DOUBLE)    AS average_180day,
                TRY_CAST("index" AS DOUBLE)          AS sofr_index
            FROM "ny-fed-reference-rates-secured"
            WHERE TRY_CAST(effectiveDate AS DATE) IS NOT NULL AND type IS NOT NULL
        ''',
    ),
]
