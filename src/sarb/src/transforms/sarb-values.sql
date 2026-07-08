WITH cleaned AS (
    SELECT
        TRY_CAST(strptime(period, '%Y/%m/%d %H:%M:%S') AS DATE) AS date,
        timeseries_code,
        measure_name,
        category_code,
        category_name,
        data_type,
        TRY_CAST(
            replace(replace(replace(value, chr(160), ''), ' ', ''), ',', '.')
            AS DOUBLE
        ) AS value
    FROM "sarb-values"
)
SELECT date, timeseries_code, measure_name, category_code,
       category_name, data_type, value
FROM cleaned
WHERE date IS NOT NULL
  AND value IS NOT NULL
  AND timeseries_code IS NOT NULL
QUALIFY row_number() OVER (
    PARTITION BY data_type, timeseries_code, date
    ORDER BY measure_name
) = 1
