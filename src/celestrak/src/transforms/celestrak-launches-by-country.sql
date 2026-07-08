SELECT
    SUBSTRING(launch_date, 1, 4) AS year,
    COALESCE(owner, 'UNKNOWN') AS country,
    SUM(CASE WHEN object_type = 'PAY' THEN 1 ELSE 0 END)::BIGINT AS payloads,
    SUM(CASE WHEN object_type = 'R/B' THEN 1 ELSE 0 END)::BIGINT AS rocket_bodies,
    SUM(CASE WHEN object_type = 'DEB' THEN 1 ELSE 0 END)::BIGINT AS debris,
    COUNT(*)::BIGINT AS total
FROM "celestrak-launches-by-country"
WHERE launch_date IS NOT NULL AND launch_date != ''
GROUP BY year, country
ORDER BY year, country
