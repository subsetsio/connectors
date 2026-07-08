SELECT industry, CAST(naics_code AS VARCHAR) AS naics_code,
       CAST(year AS INTEGER) AS year, event_type,
       CAST(fatal_count AS BIGINT) AS fatal_count
FROM "alaska-department-of-labor-and-workforce-development-workplace-fatalities"
WHERE industry IS NOT NULL AND fatal_count IS NOT NULL
