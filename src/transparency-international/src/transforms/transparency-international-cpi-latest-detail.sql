SELECT
    country,
    iso3,
    region,
    source_name,
    CAST(source_score AS DOUBLE) AS source_score
FROM "transparency-international-cpi-latest-detail"
WHERE source_score IS NOT NULL
