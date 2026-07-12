-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "experience_years_ar",
    "experience_years",
    "statement_ar",
    "statement",
    "no_of_people"
FROM "qatar-planning-and-statistics-authority-deaths-and-injuries-in-traffic-accidents-by-driver-s-experience"
