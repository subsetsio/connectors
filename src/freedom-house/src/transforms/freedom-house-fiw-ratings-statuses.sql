SELECT
    entity_kind,
    country,
    CAST(year AS INTEGER) AS year,
    CAST(pr AS INTEGER) AS pr,
    CAST(cl AS INTEGER) AS cl,
    status
FROM "freedom-house-fiw-ratings-statuses"
WHERE country IS NOT NULL AND year IS NOT NULL
  AND (pr IS NOT NULL OR cl IS NOT NULL OR status IS NOT NULL)
