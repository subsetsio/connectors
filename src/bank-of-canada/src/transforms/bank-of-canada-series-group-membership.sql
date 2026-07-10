SELECT
    group_id,
    series_id,
    series_label
FROM "bank-of-canada-series-group-membership"
WHERE group_id IS NOT NULL
  AND series_id IS NOT NULL
