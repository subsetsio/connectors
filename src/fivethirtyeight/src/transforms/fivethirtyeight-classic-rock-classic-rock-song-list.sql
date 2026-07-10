-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Song Clean" AS song_clean,
    "ARTIST CLEAN" AS artist_clean,
    "Release Year" AS release_year,
    "COMBINED" AS combined,
    "First?" AS first,
    "Year?" AS year,
    "PlayCount" AS playcount,
    "F*G" AS f_g
FROM "fivethirtyeight-classic-rock-classic-rock-song-list"
