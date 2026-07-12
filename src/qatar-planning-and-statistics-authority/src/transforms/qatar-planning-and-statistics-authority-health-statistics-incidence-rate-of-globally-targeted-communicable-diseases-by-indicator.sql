-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "indicator",
    "lmw_shr",
    "incidence_rate_per_10_000_person_of_the_population"
FROM "qatar-planning-and-statistics-authority-health-statistics-incidence-rate-of-globally-targeted-communicable-diseases-by-indicator"
