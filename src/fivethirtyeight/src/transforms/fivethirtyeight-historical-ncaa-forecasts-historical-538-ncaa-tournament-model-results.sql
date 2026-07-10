-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "round",
    "favorite",
    "underdog",
    "favorite_probability",
    "favorite_win_flag"
FROM "fivethirtyeight-historical-ncaa-forecasts-historical-538-ncaa-tournament-model-results"
