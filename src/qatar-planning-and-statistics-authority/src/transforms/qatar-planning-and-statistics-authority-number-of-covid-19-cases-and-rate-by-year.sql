-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "number_of_cases",
    "incidence_per_100_000_population"
FROM "qatar-planning-and-statistics-authority-number-of-covid-19-cases-and-rate-by-year"
