-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sex",
    "years",
    "institutions",
    "value"
FROM "geostat-gender-20statistics-education-03-number-of-schoolteachers-professors-and-lecturers"
