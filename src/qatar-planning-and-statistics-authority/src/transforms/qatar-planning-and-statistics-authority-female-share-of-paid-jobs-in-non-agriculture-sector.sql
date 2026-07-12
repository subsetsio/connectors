-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "percentage"
FROM "qatar-planning-and-statistics-authority-female-share-of-paid-jobs-in-non-agriculture-sector"
