-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_library",
    "name_of_library_ar",
    "year",
    "sn",
    "value"
FROM "qatar-planning-and-statistics-authority-public-libraries-by-number-of-borrowers-and-books-borrowed"
