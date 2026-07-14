-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("goals" AS BIGINT) AS goals,
    CAST("own_goals" AS BIGINT) AS own_goals,
    CAST("shots" AS BIGINT) AS shots,
    CAST("xG" AS DOUBLE) AS xg,
    CAST("time" AS BIGINT) AS time,
    CAST("player_id" AS BIGINT) AS player_id,
    CAST("team_id" AS BIGINT) AS team_id,
    "position",
    "player",
    "h_a",
    CAST("yellow_card" AS BIGINT) AS yellow_card,
    CAST("red_card" AS BIGINT) AS red_card,
    CAST("roster_in" AS BIGINT) AS roster_in,
    CAST("roster_out" AS BIGINT) AS roster_out,
    CAST("key_passes" AS BIGINT) AS key_passes,
    CAST("assists" AS BIGINT) AS assists,
    CAST("xA" AS DOUBLE) AS xa,
    CAST("xGChain" AS DOUBLE) AS xgchain,
    CAST("xGBuildup" AS DOUBLE) AS xgbuildup,
    CAST("positionOrder" AS BIGINT) AS positionorder,
    "league",
    "season",
    CAST("match_id" AS BIGINT) AS match_id,
    "side",
    CAST("roster_id" AS BIGINT) AS roster_id
FROM "understat-rosters"
