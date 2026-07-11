-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Region" AS region,
    "Reason" AS reason,
    "Аge group" AS ge_group,
    "Sex" AS sex,
    CAST("Year" AS BIGINT) AS year,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0400-036v0-1"
