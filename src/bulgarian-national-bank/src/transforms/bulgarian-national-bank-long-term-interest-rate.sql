-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The table contains multiple frequency/page variants of the convergence long-term interest-rate series; filter by frequency and series before time-series analysis.
SELECT
    "keyfamily",
    "freq",
    CAST("page_id" AS BIGINT) AS page_id,
    "series_key",
    "series_name",
    "period",
    "value"
FROM "bulgarian-national-bank-long-term-interest-rate"
