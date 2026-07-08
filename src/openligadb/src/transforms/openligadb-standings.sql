SELECT
    league_shortcut,
    CAST(league_season AS INTEGER) AS league_season,
    CAST(team_id AS BIGINT)        AS team_id,
    team_name,
    short_name,
    CAST(points AS INTEGER)        AS points,
    CAST(matches AS INTEGER)       AS matches,
    CAST(won AS INTEGER)           AS won,
    CAST(draw AS INTEGER)          AS draw,
    CAST(lost AS INTEGER)          AS lost,
    CAST(goals AS INTEGER)         AS goals,
    CAST(opponent_goals AS INTEGER) AS opponent_goals,
    CAST(goal_diff AS INTEGER)     AS goal_diff
FROM "openligadb-standings"
WHERE team_id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY league_shortcut, league_season, team_id ORDER BY points DESC) = 1
