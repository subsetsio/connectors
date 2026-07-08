SELECT geo_level, area_name, period,
       CAST(population AS BIGINT) AS population,
       CAST(population_change AS BIGINT) AS population_change,
       CAST(growth_rate_pct AS DOUBLE) AS growth_rate_pct,
       CAST(births AS BIGINT) AS births, CAST(deaths AS BIGINT) AS deaths,
       CAST(natural_increase AS BIGINT) AS natural_increase,
       CAST(in_migration AS BIGINT) AS in_migration,
       CAST(out_migration AS BIGINT) AS out_migration,
       CAST(net_migration AS BIGINT) AS net_migration
FROM "alaska-department-of-labor-and-workforce-development-population-components-of-change"
WHERE area_name IS NOT NULL AND population IS NOT NULL
