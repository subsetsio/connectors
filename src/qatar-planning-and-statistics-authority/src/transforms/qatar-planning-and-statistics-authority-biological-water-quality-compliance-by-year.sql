-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "biological_compliance",
    "who_target"
FROM "qatar-planning-and-statistics-authority-biological-water-quality-compliance-by-year"
