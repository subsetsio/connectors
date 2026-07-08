SELECT
    country_name,
    country_iso2,
    CAST(week AS DATE)                  AS week,
    category,
    weekly_rank,
    show_title,
    NULLIF(season_title, 'N/A')         AS season_title,
    cumulative_weeks_in_top_10
FROM "netflix-countries-weekly"
WHERE week IS NOT NULL AND weekly_rank IS NOT NULL
