SELECT
    country,
    CAST(year AS INTEGER) AS year,
    total_score,
    status,
    legal,
    political,
    economic
FROM "freedom-house-freedom-of-the-press"
WHERE country IS NOT NULL AND year IS NOT NULL
  AND (total_score IS NOT NULL OR status IS NOT NULL)
