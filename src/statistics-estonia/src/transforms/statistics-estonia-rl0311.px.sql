-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "acquired_educational_attainment",
    "sex",
    "age_group",
    "labour_status",
    "ethnic_nationality",
    "value"
FROM "statistics-estonia-rl0311.px"
