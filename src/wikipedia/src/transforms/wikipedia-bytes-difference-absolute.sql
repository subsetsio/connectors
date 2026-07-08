SELECT
    project,
    CAST(date AS DATE) AS date,
    "abs_bytes_diff"
FROM "wikipedia-bytes-difference-absolute"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "abs_bytes_diff" IS NOT NULL
