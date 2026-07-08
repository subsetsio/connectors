SELECT
    CAST(week AS DATE)                  AS week,
    category,
    weekly_rank,
    show_title,
    NULLIF(season_title, 'N/A')         AS season_title,
    weekly_hours_viewed,
    runtime                             AS runtime_hours,
    weekly_views,
    cumulative_weeks_in_top_10
FROM "netflix-global-weekly"
WHERE week IS NOT NULL AND weekly_rank IS NOT NULL
