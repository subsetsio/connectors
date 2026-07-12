-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "length_of_service_years_ar",
    "males",
    "females",
    "percentage",
    "average_age_at_retirement",
    "total",
    "length_of_service_in_years"
FROM "qatar-planning-and-statistics-authority-retirees-registered-in-pension-funds-and-systems-by-length-of-employment"
