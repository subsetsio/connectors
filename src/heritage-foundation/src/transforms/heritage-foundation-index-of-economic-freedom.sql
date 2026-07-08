SELECT
    CAST(year AS INTEGER) AS year,
    country,
    region,
    component,
    CAST(score AS DOUBLE) AS score
FROM "heritage-foundation-index-of-economic-freedom"
WHERE score IS NOT NULL
  AND country IS NOT NULL
  AND component IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY year, country, component ORDER BY score DESC
) = 1
