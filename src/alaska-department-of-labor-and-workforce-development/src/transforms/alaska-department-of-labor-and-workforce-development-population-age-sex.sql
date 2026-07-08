SELECT geo_level, area_name, CAST(bca_fips AS VARCHAR) AS bca_fips,
       CAST(place_fips AS VARCHAR) AS place_fips, age, period_label,
       CAST(year AS INTEGER) AS year, sex,
       CAST(population AS BIGINT) AS population
FROM "alaska-department-of-labor-and-workforce-development-population-age-sex"
WHERE area_name IS NOT NULL AND age IS NOT NULL AND population IS NOT NULL
