-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Contains bank financial-reporting indicators at multiple reporting frequencies; filter the frequency dimension before comparing or summing periods.
SELECT
    CAST("dt" AS BIGINT) AS dt,
    "txt",
    "txten",
    "id_api",
    "leveli",
    "parent",
    "freq",
    CAST("nkb" AS BIGINT) AS nkb,
    CAST("mfo" AS BIGINT) AS mfo,
    "fullname",
    "gr_bank",
    "r034",
    "tzep",
    "value"
FROM "national-bank-of-ukraine-banksfinrep"
