SELECT location_name, location_type, location_fips_code, population, state, county, metro,
       month AS date,
       value AS vacancy_rate
FROM "apartment-list-vacancy-index"
WHERE value IS NOT NULL
