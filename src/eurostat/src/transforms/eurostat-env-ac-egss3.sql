-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "ty",
    "na_item",
    "unit",
    "nace_r2",
    "ceparema",
    "geo",
    CAST("time_period" AS BIGINT) AS time_period,
    "value",
    "flag"
FROM "eurostat-env-ac-egss3"
