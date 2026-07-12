-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "nationality_ar",
    "type_of_consultancy",
    "type_of_consultancy_ar",
    "gender",
    "gender_ar",
    "value"
FROM "qatar-planning-and-statistics-authority-services-rendered-qatar-foundation-for-combating-human-trafficking-by-type-of-consultancy-gender-and"
