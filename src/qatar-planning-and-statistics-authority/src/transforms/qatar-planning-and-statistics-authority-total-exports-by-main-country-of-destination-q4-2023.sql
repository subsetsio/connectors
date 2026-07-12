-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "country",
    "ldwl",
    "percentage"
FROM "qatar-planning-and-statistics-authority-total-exports-by-main-country-of-destination-q4-2023"
