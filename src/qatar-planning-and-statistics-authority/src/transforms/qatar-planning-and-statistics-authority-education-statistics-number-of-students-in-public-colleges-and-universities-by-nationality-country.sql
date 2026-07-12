-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "nationality",
    "ljnsy",
    "country",
    "ldwl",
    "gender",
    "lnw",
    "number_of_students"
FROM "qatar-planning-and-statistics-authority-education-statistics-number-of-students-in-public-colleges-and-universities-by-nationality-country"
