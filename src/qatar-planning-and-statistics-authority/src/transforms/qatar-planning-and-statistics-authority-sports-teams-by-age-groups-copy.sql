-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "adults",
    "youth",
    "junior_u18",
    "junior_u16",
    "kids"
FROM "qatar-planning-and-statistics-authority-sports-teams-by-age-groups-copy"
