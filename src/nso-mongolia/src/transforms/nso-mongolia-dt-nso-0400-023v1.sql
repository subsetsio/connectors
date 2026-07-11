-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SEX" AS sex,
    "TYPES OF OWNERSHIP" AS types_of_ownership,
    CAST("TIMES (ANNUAL)" AS BIGINT) AS times_annual,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0400-023v1"
