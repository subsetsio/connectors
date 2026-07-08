SELECT
    media_type,
    CAST(date AS DATE) AS date,
    requests
FROM "wikipedia-mediarequests"
WHERE date IS NOT NULL
  AND requests IS NOT NULL
