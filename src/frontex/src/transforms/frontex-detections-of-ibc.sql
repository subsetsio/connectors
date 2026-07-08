SELECT DISTINCT
    CAST(month AS DATE)        AS month,
    route,
    border_type,
    nationality,
    CAST(detections AS BIGINT) AS detections
FROM "frontex-detections-of-ibc"
WHERE detections IS NOT NULL
  AND route IS NOT NULL
  AND nationality IS NOT NULL
