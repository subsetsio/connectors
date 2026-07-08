SELECT
    series,
    CAST(regexp_replace(year, '[^0-9]', '', 'g') AS INTEGER) AS year,
    (year LIKE '%*%') AS preliminary,
    CAST(annual_average_index AS DOUBLE) AS annual_average_index,
    TRY_CAST(replace(annual_percent_change, '%', '') AS DOUBLE)
        AS annual_percent_change
FROM "federal-reserve-bank-of-minneapolis-cpi-historical"
WHERE year IS NOT NULL
  AND regexp_replace(year, '[^0-9]', '', 'g') <> ''
  AND annual_average_index IS NOT NULL
