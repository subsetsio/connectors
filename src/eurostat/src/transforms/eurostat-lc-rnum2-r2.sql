-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "freq",
    "sizeclas",
    "worktime",
    "indic_lc",
    "nace_r2",
    "unit",
    "geo",
    CAST("time_period" AS BIGINT) AS time_period,
    "value",
    "flag"
FROM "eurostat-lc-rnum2-r2"
