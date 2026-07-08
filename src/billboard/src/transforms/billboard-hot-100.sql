SELECT
    CAST(chart_date AS DATE)        AS chart_date,
    CAST(rank AS INTEGER)           AS rank,
    song,
    artist,
    CAST(last_week AS INTEGER)      AS last_week,
    CAST(peak_position AS INTEGER)  AS peak_position,
    CAST(weeks_on_chart AS INTEGER) AS weeks_on_chart
FROM "billboard-hot-100"
WHERE chart_date IS NOT NULL
  AND rank IS NOT NULL
  AND song IS NOT NULL
  AND artist IS NOT NULL
  AND rank BETWEEN 1 AND 100
