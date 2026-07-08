SELECT
    project,
    CAST(date AS DATE) AS date,
    "editors"
FROM "wikipedia-editors"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "editors" IS NOT NULL
