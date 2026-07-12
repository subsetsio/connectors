-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "football_pitches",
    "swimming_pool",
    "indoor_halls",
    "tennis_court",
    "basketball_courts"
FROM "qatar-planning-and-statistics-authority-sports-facilities-of-qatar-olympic-committee-by-type"
