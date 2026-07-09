SELECT
    CAST(section AS VARCHAR) AS section,
    CAST(full_name AS VARCHAR) AS full_name,
    CAST(short_name AS VARCHAR) AS short_name,
    CAST(time_series AS VARCHAR) AS time_series,
    CAST(start_year AS INTEGER) AS start_year,
    CAST(end_year AS INTEGER) AS end_year,
    CAST(is_group AS BOOLEAN) AS is_group
FROM "undp-indicators"
WHERE full_name IS NOT NULL
