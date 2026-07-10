-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "yearID" AS yearid,
    "gameNum" AS gamenum,
    "gameID" AS gameid,
    "lgID" AS lgid,
    "tm_OFF_talent" AS tm_off_talent,
    "tm_DEF_talent" AS tm_def_talent,
    "tm_PIT_talent" AS tm_pit_talent,
    "MLB_avg_RPG" AS mlb_avg_rpg,
    "talent_RSPG" AS talent_rspg,
    "talent_RAPG" AS talent_rapg,
    "unadj_PYTH" AS unadj_pyth,
    "timeline_adj",
    "SOS" AS sos,
    "adj_PYTH" AS adj_pyth,
    "no_1_player",
    "no_2_player"
FROM "fivethirtyeight-mlb-allstar-teams-allstar-team-talent"
