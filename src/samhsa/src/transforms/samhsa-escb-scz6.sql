SELECT
    CAST(locationabbr AS VARCHAR)          AS location_code,
    CAST(locationdesc AS VARCHAR)          AS location,
    TRY_CAST(ffy_year AS INTEGER)          AS federal_fiscal_year,
    CAST(topicdesc AS VARCHAR)             AS topic,
    CAST(measuredesc AS VARCHAR)           AS measure,
    CAST(submeasure AS VARCHAR)            AS submeasure,
    TRY_CAST(data_value AS DOUBLE)         AS value,
    CAST(data_value_unit AS VARCHAR)       AS unit,
    CAST(data_value_type AS VARCHAR)       AS value_type,
    CAST(source AS VARCHAR)                AS source
FROM "samhsa-escb-scz6"
WHERE TRY_CAST(data_value AS DOUBLE) IS NOT NULL
  AND TRY_CAST(ffy_year AS INTEGER) IS NOT NULL
