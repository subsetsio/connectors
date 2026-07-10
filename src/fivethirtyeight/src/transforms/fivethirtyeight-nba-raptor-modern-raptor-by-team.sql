-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "player_name",
    "player_id",
    "season",
    "season_type",
    "team",
    "poss",
    "mp",
    "raptor_box_offense",
    "raptor_box_defense",
    "raptor_box_total",
    "raptor_onoff_offense",
    "raptor_onoff_defense",
    "raptor_onoff_total",
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
FROM "fivethirtyeight-nba-raptor-modern-raptor-by-team"
