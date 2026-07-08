SELECT geo_level, area_name, CAST(fips AS VARCHAR) AS fips, period,
       CAST(year AS INTEGER) AS year, CAST(population AS BIGINT) AS population
FROM "alaska-department-of-labor-and-workforce-development-population-total"
WHERE area_name IS NOT NULL AND population IS NOT NULL
