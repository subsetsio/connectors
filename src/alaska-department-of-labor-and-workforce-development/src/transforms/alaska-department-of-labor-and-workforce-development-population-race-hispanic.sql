SELECT geo_level, area_name, CAST(fips AS VARCHAR) AS fips,
       CAST(year AS INTEGER) AS year, race,
       CAST(population AS BIGINT) AS population
FROM "alaska-department-of-labor-and-workforce-development-population-race-hispanic"
WHERE area_name IS NOT NULL AND race IS NOT NULL AND population IS NOT NULL
