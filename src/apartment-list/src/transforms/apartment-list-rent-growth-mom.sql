SELECT location_name, location_type, location_fips_code, population, state, county, metro,
       month AS date,
       value AS rent_growth_mom
FROM "apartment-list-rent-growth-mom"
WHERE value IS NOT NULL
