SELECT
    indicator_code,
    name,
    theme,
    last_data_update,
    last_data_update_description,
    CAST(total_record_count AS BIGINT) AS total_record_count,
    CAST(year_min AS INTEGER)          AS year_min,
    CAST(year_max AS INTEGER)          AS year_max,
    geo_unit_types
FROM "unesco-institute-for-statistics-indicators"
WHERE indicator_code IS NOT NULL
