-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are league-season player summaries, not one row per player identity; a player can appear in multiple seasons or leagues.
SELECT
    CAST("id" AS BIGINT) AS id,
    "player_name",
    CAST("games" AS BIGINT) AS games,
    CAST("time" AS BIGINT) AS time,
    CAST("goals" AS BIGINT) AS goals,
    CAST("xG" AS DOUBLE) AS xg,
    CAST("assists" AS BIGINT) AS assists,
    CAST("xA" AS DOUBLE) AS xa,
    CAST("shots" AS BIGINT) AS shots,
    CAST("key_passes" AS BIGINT) AS key_passes,
    CAST("yellow_cards" AS BIGINT) AS yellow_cards,
    CAST("red_cards" AS BIGINT) AS red_cards,
    "position",
    "team_title",
    CAST("npg" AS BIGINT) AS npg,
    CAST("npxG" AS DOUBLE) AS npxg,
    CAST("xGChain" AS DOUBLE) AS xgchain,
    CAST("xGBuildup" AS DOUBLE) AS xgbuildup,
    "league",
    "season"
FROM "understat-players"
