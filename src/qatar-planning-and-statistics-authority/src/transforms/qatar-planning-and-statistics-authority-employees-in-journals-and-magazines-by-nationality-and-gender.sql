-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "name_of_library",
    "name_of_library_ar",
    "no_of_employees"
FROM "qatar-planning-and-statistics-authority-employees-in-journals-and-magazines-by-nationality-and-gender"
