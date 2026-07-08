SELECT
    region,
    region_code,
    CAST(year AS INTEGER)        AS year,
    CAST(harvest_date AS DOUBLE) AS harvest_date
FROM "grape-harvest-dates-harvest-dates"
WHERE harvest_date IS NOT NULL
