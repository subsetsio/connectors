-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "five_star",
    "four_star",
    "three_star",
    "two_one_star"
FROM "qatar-planning-and-statistics-authority-number-of-hotel-beds-by-hotel-class"
