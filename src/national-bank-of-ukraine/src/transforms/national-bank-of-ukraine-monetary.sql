-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains monetary aggregates and components in one hierarchy; filter the indicator hierarchy before summing to avoid double counting.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    "k076",
    CAST("ind" AS BIGINT) AS ind,
    "tzep",
    "value"
FROM "national-bank-of-ukraine-monetary"
