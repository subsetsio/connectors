SELECT location_name, location_type, location_fips_code, population, state, county, metro,
       month AS date,
       value AS days_on_market
FROM "apartment-list-time-on-market"
WHERE value IS NOT NULL
