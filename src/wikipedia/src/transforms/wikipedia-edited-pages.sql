SELECT
    project,
    CAST(date AS DATE) AS date,
    "edited_pages"
FROM "wikipedia-edited-pages"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "edited_pages" IS NOT NULL
