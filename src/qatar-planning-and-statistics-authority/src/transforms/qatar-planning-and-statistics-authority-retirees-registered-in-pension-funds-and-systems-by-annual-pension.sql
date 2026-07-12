-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "males",
    "females",
    "percentage",
    "average_age_at_retirement",
    "annual_pension"
FROM "qatar-planning-and-statistics-authority-retirees-registered-in-pension-funds-and-systems-by-annual-pension"
