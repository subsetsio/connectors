SELECT geo_level, scenario, period_label, CAST(year AS INTEGER) AS year,
       CAST(is_projected AS BOOLEAN) AS is_projected, age, sex,
       CAST(population AS BIGINT) AS population
FROM "alaska-department-of-labor-and-workforce-development-population-projections"
WHERE year IS NOT NULL AND age IS NOT NULL AND population IS NOT NULL
