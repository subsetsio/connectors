-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "live_births",
    "deaths",
    "natural_increase"
FROM "qatar-planning-and-statistics-authority-registered-vital-events"
