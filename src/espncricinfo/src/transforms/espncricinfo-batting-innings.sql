SELECT
    TRY_CAST(event_id AS BIGINT)  AS event_id,
    TRY_CAST(league_id AS BIGINT) AS league_id,
    TRY_CAST(innings AS INTEGER)  AS innings,
    team,
    TRY_CAST(player_id AS BIGINT) AS player_id,
    player_name,
    TRY_CAST(runs AS INTEGER)     AS runs,
    TRY_CAST(balls AS INTEGER)    AS balls,
    TRY_CAST(fours AS INTEGER)    AS fours,
    TRY_CAST(sixes AS INTEGER)    AS sixes,
    TRY_CAST(strike_rate AS DOUBLE) AS strike_rate,
    TRY_CAST(batting_position AS INTEGER) AS batting_position,
    TRY_CAST(not_out AS INTEGER)  AS not_out,
    dismissal
FROM "espncricinfo-batting-innings"
WHERE TRY_CAST(player_id AS BIGINT) IS NOT NULL
  AND TRY_CAST(event_id AS BIGINT) IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY event_id, innings, player_id ORDER BY runs DESC
) = 1
