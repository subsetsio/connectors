-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "gameorder",
    "game_id",
    "lg_id",
    "_iscopy" AS iscopy,
    "year_id",
    "date_game",
    "seasongame",
    "is_playoffs",
    "team_id",
    "fran_id",
    "pts",
    "elo_i",
    "elo_n",
    "win_equiv",
    "opp_id",
    "opp_fran",
    "opp_pts",
    "opp_elo_i",
    "opp_elo_n",
    "game_location",
    "game_result",
    "forecast",
    "notes"
FROM "fivethirtyeight-nba-elo-nbaallelo"
