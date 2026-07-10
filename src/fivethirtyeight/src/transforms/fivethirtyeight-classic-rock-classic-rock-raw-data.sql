-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "SONG RAW" AS song_raw,
    "Song Clean" AS song_clean,
    "ARTIST RAW" AS artist_raw,
    "ARTIST CLEAN" AS artist_clean,
    "CALLSIGN" AS callsign,
    "TIME" AS time,
    "UNIQUE_ID" AS unique_id,
    "COMBINED" AS combined,
    "First?" AS first
FROM "fivethirtyeight-classic-rock-classic-rock-raw-data"
