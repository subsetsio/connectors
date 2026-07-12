-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_perceptions",
    "smokers_type",
    "percentage_of_people"
FROM "qatar-planning-and-statistics-authority-percentage-of-perceptions-on-smoking-by-smoker-type"
