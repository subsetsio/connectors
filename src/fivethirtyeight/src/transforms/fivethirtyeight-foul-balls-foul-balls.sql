-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "matchup",
    "game_date",
    "type_of_hit",
    "exit_velocity",
    "predicted_zone",
    "camera_zone",
    "used_zone"
FROM "fivethirtyeight-foul-balls-foul-balls"
