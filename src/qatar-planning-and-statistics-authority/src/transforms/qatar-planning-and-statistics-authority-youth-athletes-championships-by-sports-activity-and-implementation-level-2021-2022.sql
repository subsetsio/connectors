-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "sports_activity_ar",
    "domestic",
    "international",
    "asian",
    "arab",
    "gcc"
FROM "qatar-planning-and-statistics-authority-youth-athletes-championships-by-sports-activity-and-implementation-level-2021-2022"
