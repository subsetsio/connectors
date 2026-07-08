SELECT CAST(census_year AS INTEGER) AS census_year,
       urbanized_area,
       CAST(population AS BIGINT) AS population,
       CAST(land_area_sq_mi AS DOUBLE) AS land_area_sq_mi,
       CAST(density_per_sq_mi AS DOUBLE) AS density_per_sq_mi,
       primary_state, secondary_state, third_state, fourth_state
FROM "american-public-transportation-association-factbook-c-uza-population-by-census-year"
WHERE urbanized_area IS NOT NULL
