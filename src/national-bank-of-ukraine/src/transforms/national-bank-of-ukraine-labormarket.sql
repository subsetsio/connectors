-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains monthly and quarterly labour-market observations in one long table; filter frequency before comparing or aggregating periods.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    "mcr210i",
    "mcrk110",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-labormarket"
