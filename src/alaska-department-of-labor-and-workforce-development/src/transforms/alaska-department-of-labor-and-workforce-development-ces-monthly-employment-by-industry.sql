SELECT area_name, CAST(area_code AS VARCHAR) AS area_code,
       CAST(COALESCE(seasonally_adjusted, 0) AS BOOLEAN) AS seasonally_adjusted,
       CAST(series_code AS VARCHAR) AS series_code, industry,
       CAST(year AS INTEGER) AS year, CAST(month AS INTEGER) AS month,
       CAST(employment AS BIGINT) AS employment
FROM "alaska-department-of-labor-and-workforce-development-ces-monthly-employment-by-industry"
WHERE year IS NOT NULL AND month IS NOT NULL AND employment IS NOT NULL
