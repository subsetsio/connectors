-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "sports_activity",
    "lnsht_lrydy",
    "adults",
    "youth",
    "junior_u18",
    "junior_u16",
    "kids",
    "total"
FROM "qatar-planning-and-statistics-authority-arab-championships-by-sports-activity-and-age-groups-2023"
