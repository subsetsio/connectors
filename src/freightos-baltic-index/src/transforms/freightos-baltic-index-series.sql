SELECT DISTINCT
    index_code,
    name,
    unit,
    currency,
    frequency,
    CAST(first_date AS DATE) AS first_date,
    CAST(last_date AS DATE) AS last_date,
    observation_count
FROM "freightos-baltic-index-series"
WHERE index_code IS NOT NULL
