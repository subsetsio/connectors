-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pfr_player_id",
    "player_name",
    "career_try",
    "career_ranypa",
    "career_wowy",
    "bcs_rating"
FROM "fivethirtyeight-nfl-wide-receivers-advanced-historical"
