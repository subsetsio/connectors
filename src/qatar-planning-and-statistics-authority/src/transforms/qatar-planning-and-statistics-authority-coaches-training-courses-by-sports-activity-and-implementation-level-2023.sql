-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activity_ar",
    "domestic",
    "gulf",
    "arab",
    "asian",
    "international",
    "total"
FROM "qatar-planning-and-statistics-authority-coaches-training-courses-by-sports-activity-and-implementation-level-2023"
