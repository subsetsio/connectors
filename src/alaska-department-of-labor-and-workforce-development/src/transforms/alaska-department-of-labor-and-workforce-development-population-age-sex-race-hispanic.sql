SELECT geo_level, race_basis, area_name, CAST(fips AS VARCHAR) AS fips,
       age, CAST(year AS INTEGER) AS year, race, sex,
       CAST(population AS BIGINT) AS population
FROM "alaska-department-of-labor-and-workforce-development-population-age-sex-race-hispanic"
WHERE area_name IS NOT NULL AND age IS NOT NULL AND population IS NOT NULL
