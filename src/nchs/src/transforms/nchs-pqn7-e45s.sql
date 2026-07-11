-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "survey_years",
    "sex",
    "age_group",
    "race_and_hispanic_origin",
    "infectious_disease",
    "percent",
    "standard_error",
    "lower_95_ci_limit",
    "upper_95_ci_limit",
    "presentation_standard",
    "note1",
    "notea"
FROM "nchs-pqn7-e45s"
