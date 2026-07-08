SELECT
    region,
    region_code,
    CAST(latitude AS DOUBLE)  AS latitude,
    CAST(longitude AS DOUBLE) AS longitude
FROM "grape-harvest-dates-regions"
