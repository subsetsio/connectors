SELECT
    areaid,
    area_name,
    area_type,
    CAST(year AS INTEGER) AS year,
    CAST(records AS BIGINT) AS records
FROM "obis-statistics-by-area-year"
WHERE areaid IS NOT NULL AND year IS NOT NULL
