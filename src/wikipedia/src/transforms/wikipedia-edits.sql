SELECT
    project,
    CAST(date AS DATE) AS date,
    "edits"
FROM "wikipedia-edits"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "edits" IS NOT NULL
