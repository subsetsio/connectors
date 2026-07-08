SELECT
    CAST(match_id AS BIGINT)             AS match_id,
    league_shortcut,
    CAST(league_season AS INTEGER)       AS league_season,
    CAST(league_id AS BIGINT)            AS league_id,
    league_name,
    CAST(matchday AS INTEGER)            AS matchday,
    matchday_name,
    CAST(match_datetime_utc AS TIMESTAMP) AS match_datetime_utc,
    CAST(match_is_finished AS BOOLEAN)   AS match_is_finished,
    CAST(team1_id AS BIGINT)             AS team1_id,
    team1_name,
    CAST(team2_id AS BIGINT)             AS team2_id,
    team2_name,
    CAST(halftime_team1 AS INTEGER)      AS halftime_team1,
    CAST(halftime_team2 AS INTEGER)      AS halftime_team2,
    CAST(final_team1 AS INTEGER)         AS final_team1,
    CAST(final_team2 AS INTEGER)         AS final_team2,
    location_city,
    location_stadium,
    CAST(number_of_viewers AS BIGINT)    AS number_of_viewers
FROM "openligadb-matches"
WHERE match_id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY match_id ORDER BY last_update DESC NULLS LAST) = 1
