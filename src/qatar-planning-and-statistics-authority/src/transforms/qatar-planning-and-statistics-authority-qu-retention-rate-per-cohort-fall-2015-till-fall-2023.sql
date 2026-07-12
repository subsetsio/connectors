-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "cohort",
    "male",
    "female",
    "all"
FROM "qatar-planning-and-statistics-authority-qu-retention-rate-per-cohort-fall-2015-till-fall-2023"
