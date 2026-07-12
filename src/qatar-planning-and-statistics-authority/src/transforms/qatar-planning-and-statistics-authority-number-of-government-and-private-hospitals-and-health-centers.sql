-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "government_hospitals",
    "private_hospitals",
    "health_centers"
FROM "qatar-planning-and-statistics-authority-number-of-government-and-private-hospitals-and-health-centers"
