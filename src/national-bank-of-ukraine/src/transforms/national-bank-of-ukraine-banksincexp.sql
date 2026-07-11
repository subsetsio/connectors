-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains income and expense indicators at multiple reporting frequencies; filter the frequency dimension before comparing or summing periods.
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
FROM "national-bank-of-ukraine-banksincexp"
