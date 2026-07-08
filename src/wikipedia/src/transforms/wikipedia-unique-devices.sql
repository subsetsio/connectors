SELECT
    project,
    CAST(date AS DATE) AS date,
    "devices", "offset", "underestimate"
FROM "wikipedia-unique-devices"
WHERE project IS NOT NULL
  AND date IS NOT NULL
  AND "devices" IS NOT NULL
