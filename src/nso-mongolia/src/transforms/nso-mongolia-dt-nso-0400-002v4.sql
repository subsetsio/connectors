-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Age group" AS age_group,
    "Region" AS region,
    "Sex" AS sex,
    "Month" AS month,
    "value",
    "unit"
FROM "nso-mongolia-dt-nso-0400-002v4"
