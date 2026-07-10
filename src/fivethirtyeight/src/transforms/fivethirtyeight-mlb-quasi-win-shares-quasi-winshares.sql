-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "name_common",
    "age",
    "player_ID" AS player_id,
    "year_ID" AS year_id,
    "team_ID" AS team_id,
    "lg_ID" AS lg_id,
    "pct_PT" AS pct_pt,
    "WAR162" AS war162,
    "def_pos",
    "quasi_ws",
    "stint_ID" AS stint_id,
    "franch_id",
    "prev_franch",
    "year_acq",
    "year_left",
    "next_franch"
FROM "fivethirtyeight-mlb-quasi-win-shares-quasi-winshares"
