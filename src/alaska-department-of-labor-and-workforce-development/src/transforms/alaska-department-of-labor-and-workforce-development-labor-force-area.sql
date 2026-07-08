SELECT area_name, area_type, CAST(area_code AS VARCHAR) AS area_code,
       CAST(year AS INTEGER) AS year, month, CAST(period AS INTEGER) AS period,
       CAST(COALESCE(preliminary, 0) AS BOOLEAN) AS preliminary,
       CAST(labor_force AS BIGINT) AS labor_force,
       CAST(employment AS BIGINT) AS employment,
       CAST(unemployment AS BIGINT) AS unemployment,
       CAST(unemployment_rate AS DOUBLE) AS unemployment_rate
FROM "alaska-department-of-labor-and-workforce-development-labor-force-area"
WHERE year IS NOT NULL
  AND (labor_force IS NOT NULL OR unemployment_rate IS NOT NULL)
