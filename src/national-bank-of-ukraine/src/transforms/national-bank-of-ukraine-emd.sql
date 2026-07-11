-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains currency-in-circulation observations across denomination and instrument dimensions; filter dimensions before summing to avoid mixing totals and components.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    "z060",
    "z061",
    "z053",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-emd"
