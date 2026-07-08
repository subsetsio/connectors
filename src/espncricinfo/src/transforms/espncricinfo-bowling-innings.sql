SELECT
    TRY_CAST(event_id AS BIGINT)  AS event_id,
    TRY_CAST(league_id AS BIGINT) AS league_id,
    TRY_CAST(innings AS INTEGER)  AS innings,
    team,
    TRY_CAST(player_id AS BIGINT) AS player_id,
    player_name,
    TRY_CAST(overs AS DOUBLE)     AS overs,
    TRY_CAST(maidens AS INTEGER)  AS maidens,
    TRY_CAST(runs_conceded AS INTEGER) AS runs_conceded,
    TRY_CAST(wickets AS INTEGER)  AS wickets,
    TRY_CAST(economy AS DOUBLE)   AS economy,
    TRY_CAST(wides AS INTEGER)    AS wides,
    TRY_CAST(noballs AS INTEGER)  AS noballs,
    TRY_CAST(dots AS INTEGER)     AS dots,
    TRY_CAST(bowling_position AS INTEGER) AS bowling_position
FROM "espncricinfo-bowling-innings"
WHERE TRY_CAST(player_id AS BIGINT) IS NOT NULL
  AND TRY_CAST(event_id AS BIGINT) IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY event_id, innings, player_id ORDER BY wickets DESC
) = 1
