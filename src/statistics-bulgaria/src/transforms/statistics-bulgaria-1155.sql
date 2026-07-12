-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "period",
    "d_10_years_age_groups_lfs",
    "internatonal_standard_classification_of_education_r_d",
    "unit",
    "value"
FROM "statistics-bulgaria-1155"
