-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains daily liquidity indicators in source hierarchy form; filter the indicator hierarchy before summing to avoid mixing totals and components.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-liquidity"
