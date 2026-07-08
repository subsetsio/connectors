SELECT
    CAST(position AS INTEGER)            AS position,
    CAST(prior_year_position AS INTEGER) AS prior_year_position,
    language,
    CAST(rating_pct AS DOUBLE)           AS rating_pct,
    CAST(change_pct AS DOUBLE)           AS change_pct
FROM "tiobe-current-rankings"
WHERE position IS NOT NULL AND language IS NOT NULL
