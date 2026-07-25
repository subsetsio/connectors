-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Series keys encode SDMX dimensions; filter to the intended series before comparing or aggregating observations.
SELECT
    "keyfamily",
    "freq",
    CAST("page_id" AS BIGINT) AS page_id,
    "series_key",
    "series_name",
    "period",
    "value"
FROM "bulgarian-national-bank-direct-investment-abroad"
