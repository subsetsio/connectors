SELECT
    CAST(league_id AS BIGINT)       AS league_id,
    league_name,
    league_shortcut,
    CAST(league_season AS INTEGER)  AS league_season,
    CAST(sport_id AS BIGINT)        AS sport_id,
    sport_name
FROM "openligadb-leagues"
WHERE league_id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY league_id ORDER BY league_season DESC NULLS LAST) = 1
