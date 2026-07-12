-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "college",
    "college_ar",
    "field_of_specialization",
    "field_of_specialization_ar",
    "qataris",
    "non_qataris"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-graduates-of-public-colleges-and-universities-by-educational"
