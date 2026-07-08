SELECT
    league_shortcut,
    CAST(league_season AS INTEGER) AS league_season,
    CAST(goal_getter_id AS BIGINT) AS goal_getter_id,
    goal_getter_name,
    CAST(goal_count AS INTEGER)    AS goal_count
FROM "openligadb-goalgetters"
WHERE goal_getter_id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY league_shortcut, league_season, goal_getter_id ORDER BY goal_count DESC) = 1
