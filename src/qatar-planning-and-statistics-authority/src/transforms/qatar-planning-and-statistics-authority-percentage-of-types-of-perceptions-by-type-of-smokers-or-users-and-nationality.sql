-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_perceptions",
    "nationality",
    "percentage_of_non_smokers_users",
    "percentage_of_current_smokers_users",
    "total"
FROM "qatar-planning-and-statistics-authority-percentage-of-types-of-perceptions-by-type-of-smokers-or-users-and-nationality"
