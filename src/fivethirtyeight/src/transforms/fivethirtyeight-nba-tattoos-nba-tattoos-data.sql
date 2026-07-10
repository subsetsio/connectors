-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Player Name" AS player_name,
    "Tattoos yes/no" AS tattoos_yes_no
FROM "fivethirtyeight-nba-tattoos-nba-tattoos-data"
