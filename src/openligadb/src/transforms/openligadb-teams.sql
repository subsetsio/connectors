SELECT
    league_shortcut,
    CAST(league_season AS INTEGER) AS league_season,
    CAST(team_id AS BIGINT)        AS team_id,
    team_name,
    short_name,
    team_icon_url,
    team_group_name
FROM "openligadb-teams"
WHERE team_id IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY league_shortcut, league_season, team_id
    ORDER BY team_name
) = 1
