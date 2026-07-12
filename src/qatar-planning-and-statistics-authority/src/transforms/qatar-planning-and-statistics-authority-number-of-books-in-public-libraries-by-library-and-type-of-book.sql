-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_of_library",
    "name_of_library_ar",
    "2019_arabic_books",
    "2019_foreign_books",
    "2019_periodicals",
    "2020_arabic_books",
    "2020_foreign_books",
    "2020_periodicals",
    "2021_arabic_books",
    "2021_foreign_books",
    "2021_periodicals",
    "2022_arabic_books",
    "2022_foreign_books",
    "2022_periodicals",
    "2023_arabic_books",
    "2023_foreign_books",
    "2023_periodicals"
FROM "qatar-planning-and-statistics-authority-number-of-books-in-public-libraries-by-library-and-type-of-book"
