-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains account turnover and balance observations across account, currency, and reporting dimensions; filter dimensions before summing to avoid mixing totals and components.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    CAST("nkb" AS BIGINT) AS nkb,
    CAST("r020" AS BIGINT) AS r020,
    CAST("r034" AS BIGINT) AS r034,
    CAST("t025" AS BIGINT) AS t025,
    "tzep",
    "value"
FROM "national-bank-of-ukraine-osb"
