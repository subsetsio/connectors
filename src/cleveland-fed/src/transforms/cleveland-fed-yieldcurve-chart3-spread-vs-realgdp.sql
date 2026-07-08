SELECT TRY_CAST(date AS DATE) AS date, CASE WHEN recession > 0 THEN 1 ELSE 0 END AS recession, * EXCLUDE (date, recession) FROM "cleveland-fed-yieldcurve-chart3-spread-vs-realgdp"
