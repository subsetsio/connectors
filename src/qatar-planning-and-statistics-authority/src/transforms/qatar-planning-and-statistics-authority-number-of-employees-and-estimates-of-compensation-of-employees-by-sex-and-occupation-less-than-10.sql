-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occupation",
    "number_of_male_employees",
    "number_of_female_employees",
    "wages_salaries_qr_000",
    "payments_in_kind",
    "occupation_ar"
FROM "qatar-planning-and-statistics-authority-number-of-employees-and-estimates-of-compensation-of-employees-by-sex-and-occupation-less-than-10"
