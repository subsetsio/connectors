-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains other-financial-corporation sectoral balance-sheet indicators and components in one long table; filter indicator hierarchy before summing to avoid double counting.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    "tzep",
    "nomernb",
    "value"
FROM "national-bank-of-ukraine-sr4"
