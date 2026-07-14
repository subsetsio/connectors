-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is derived from the roster payload at the same roster_id grain as understat-rosters; do not combine it with roster measures without accounting for overlap.
SELECT
    CAST("xGChain" AS DOUBLE) AS xgchain,
    CAST("key_passes" AS BIGINT) AS key_passes,
    CAST("xGBuildup" AS DOUBLE) AS xgbuildup,
    CAST("time" AS BIGINT) AS time,
    CAST("yellow_card" AS BIGINT) AS yellow_card,
    "position",
    CAST("team_id" AS BIGINT) AS team_id,
    CAST("xG" AS DOUBLE) AS xg,
    "player",
    "h_a",
    CAST("red_card" AS BIGINT) AS red_card,
    CAST("shots" AS BIGINT) AS shots,
    CAST("player_id" AS BIGINT) AS player_id,
    CAST("assists" AS BIGINT) AS assists,
    CAST("own_goals" AS BIGINT) AS own_goals,
    CAST("goals" AS BIGINT) AS goals,
    CAST("positionOrder" AS BIGINT) AS positionorder,
    CAST("xA" AS DOUBLE) AS xa,
    "league",
    "season",
    CAST("match_id" AS BIGINT) AS match_id,
    "side",
    CAST("roster_id" AS BIGINT) AS roster_id
FROM "understat-player-match-stats"
