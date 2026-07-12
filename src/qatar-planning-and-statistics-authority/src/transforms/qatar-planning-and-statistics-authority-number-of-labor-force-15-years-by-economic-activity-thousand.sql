-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "construction",
    "public_administration"
FROM "qatar-planning-and-statistics-authority-number-of-labor-force-15-years-by-economic-activity-thousand"
