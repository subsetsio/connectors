-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "_year" AS year,
    "demographic",
    "category",
    "crisis_services",
    "crisis_services_1",
    "transitional_independent_living_til",
    "transitional_independent_living_til_1"
FROM "nyc-open-data-39et-rijq"
