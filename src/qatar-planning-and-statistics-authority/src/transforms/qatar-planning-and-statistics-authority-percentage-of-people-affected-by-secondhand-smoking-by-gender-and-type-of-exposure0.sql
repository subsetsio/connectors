-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "type_of_secondhand_smoke_exposure",
    "type_of_secondhand_smoke_exposure_ar",
    "of_female_users",
    "of_male_users",
    "overall"
FROM "qatar-planning-and-statistics-authority-percentage-of-people-affected-by-secondhand-smoking-by-gender-and-type-of-exposure0"
