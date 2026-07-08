SELECT
    TRY_CAST(event_id AS BIGINT)        AS event_id,
    TRY_CAST(league_id AS BIGINT)       AS league_id,
    league_name,
    format,
    match_class,
    -- ESPN stamps "YYYY-MM-DDTHH:MMZ" (and occasionally with seconds);
    -- neither parses via a plain TIMESTAMP cast, so try both formats.
    coalesce(
        try_strptime(date, '%Y-%m-%dT%H:%MZ'),
        try_strptime(date, '%Y-%m-%dT%H:%M:%SZ')
    )                                   AS start_time,
    CAST(substr(date, 1, 10) AS DATE)   AS match_date,
    TRY_CAST(season AS INTEGER)         AS season,
    venue, city, country,
    home_team, away_team,
    home_score, away_score, winner_team,
    status, description
FROM "espncricinfo-matches"
WHERE TRY_CAST(event_id AS BIGINT) IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY event_id ORDER BY status
) = 1
