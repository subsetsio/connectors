SELECT
    category,
    rank,
    show_title,
    NULLIF(season_title, 'N/A')         AS season_title,
    hours_viewed_first_91_days,
    runtime                             AS runtime_hours,
    views_first_91_days
FROM "netflix-most-popular"
WHERE rank IS NOT NULL
