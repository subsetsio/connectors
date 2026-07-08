SELECT
    series,
    series_description,
    goal,
    target,
    indicator,
    geo_area_code,
    geo_area_name,
    time_period AS year,
    TRY_CAST(value AS DOUBLE) AS value,
    value_type,
    source
FROM "un-statistics-division-sdg-data"
WHERE TRY_CAST(value AS DOUBLE) IS NOT NULL
  AND time_period IS NOT NULL
