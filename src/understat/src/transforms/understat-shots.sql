-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("minute" AS BIGINT) AS minute,
    "result",
    CAST("X" AS DOUBLE) AS x,
    CAST("Y" AS DOUBLE) AS y,
    CAST("xG" AS DOUBLE) AS xg,
    "player",
    "h_a",
    CAST("player_id" AS BIGINT) AS player_id,
    "situation",
    "season",
    "shotType" AS shottype,
    CAST("match_id" AS BIGINT) AS match_id,
    "h_team",
    "a_team",
    CAST("h_goals" AS BIGINT) AS h_goals,
    CAST("a_goals" AS BIGINT) AS a_goals,
    "date",
    "player_assisted",
    "lastAction" AS lastaction,
    "league",
    "side"
FROM "understat-shots"
