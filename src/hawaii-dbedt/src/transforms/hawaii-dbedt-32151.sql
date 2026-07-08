SELECT
    CAST(series_id AS BIGINT)                       AS series_id,
    series_name,
    title,
    TRY_CAST(NULLIF(measurement_id, '') AS BIGINT)  AS measurement_id,
    NULLIF(measurement_name, '')                    AS measurement_name,
    NULLIF(frequency, '')                           AS frequency,
    NULLIF(units_label, '')                         AS units_label,
    NULLIF(seasonal_adjustment, '')                 AS seasonal_adjustment,
    NULLIF(geo_fips, '')                            AS geo_fips,
    NULLIF(geo_name, '')                            AS geo_name,
    NULLIF(geo_handle, '')                          AS geo_handle,
    NULLIF(source_description, '')                  AS source_description,
    CAST(date AS DATE)                              AS date,
    CAST(value AS DOUBLE)                           AS value
FROM "hawaii-dbedt-32151"
WHERE value IS NOT NULL
  AND value <> ''
  AND TRY_CAST(value AS DOUBLE) IS NOT NULL
