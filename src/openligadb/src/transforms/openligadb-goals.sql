SELECT
    CAST(goal_id AS BIGINT)        AS goal_id,
    CAST(match_id AS BIGINT)       AS match_id,
    league_shortcut,
    CAST(league_season AS INTEGER) AS league_season,
    CAST(score_team1 AS INTEGER)   AS score_team1,
    CAST(score_team2 AS INTEGER)   AS score_team2,
    CAST(match_minute AS INTEGER)  AS match_minute,
    CAST(goal_getter_id AS BIGINT) AS goal_getter_id,
    goal_getter_name,
    CAST(is_penalty AS BOOLEAN)    AS is_penalty,
    CAST(is_own_goal AS BOOLEAN)   AS is_own_goal,
    CAST(is_overtime AS BOOLEAN)   AS is_overtime,
    comment
FROM "openligadb-goals"
WHERE goal_id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY goal_id ORDER BY goal_id) = 1
