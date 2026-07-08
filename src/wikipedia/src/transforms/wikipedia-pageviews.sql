SELECT
    project,
    CAST(date AS DATE) AS date,
    "views"
FROM "wikipedia-pageviews"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "views" IS NOT NULL
