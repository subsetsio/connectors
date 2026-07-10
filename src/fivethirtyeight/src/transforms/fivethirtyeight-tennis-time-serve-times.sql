-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "server",
    "seconds_before_next_point",
    "day",
    "opponent",
    "game_score",
    "set",
    "game"
FROM "fivethirtyeight-tennis-time-serve-times"
