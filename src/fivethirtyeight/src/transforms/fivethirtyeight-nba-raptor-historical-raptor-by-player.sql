-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "player_name",
    "player_id",
    "season",
    "poss",
    "mp",
    "raptor_offense",
    "raptor_defense",
    "raptor_total",
    "war_total",
    "war_reg_season",
    "war_playoffs",
    "predator_offense",
    "predator_defense",
    "predator_total",
    "pace_impact"
FROM "fivethirtyeight-nba-raptor-historical-raptor-by-player"
