-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "exchangedate",
    "r030",
    "cc",
    "txt",
    "enname",
    "rate",
    "units",
    "rate_per_unit",
    CAST("group" AS BIGINT) AS group,
    "calcdate",
    "special"
FROM "national-bank-of-ukraine-official-exchange-rates"
