-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "candidate",
    "song",
    "artist",
    "sentiment",
    "theme",
    "album_release_date",
    "line",
    "url"
FROM "fivethirtyeight-hip-hop-candidate-lyrics-genius-hip-hop-lyrics"
