-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "age",
    "c_work",
    "sex",
    "unit",
    "geo",
    CAST("time_period" AS BIGINT) AS time_period,
    "value",
    "flag"
FROM "eurostat-lfst-r-lfe2ecomm"
