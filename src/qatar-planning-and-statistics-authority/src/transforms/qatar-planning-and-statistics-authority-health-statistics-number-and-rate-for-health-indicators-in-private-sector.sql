-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator_ar",
    "indicator",
    "rate_per_1_000_person_of_the_population",
    "number"
FROM "qatar-planning-and-statistics-authority-health-statistics-number-and-rate-for-health-indicators-in-private-sector"
