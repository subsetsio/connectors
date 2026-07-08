SELECT location_name, location_type, location_fips_code, population, state, county, metro,
       make_date(year, month, 1) AS date,
       rent_change_mom,
       rent_change_yoy,
       CAST(price_overall AS INTEGER) AS price_overall,
       CAST(price_1br AS INTEGER)     AS price_1br,
       CAST(price_2br AS INTEGER)     AS price_2br
FROM "apartment-list-rent-estimates-summary"
WHERE year IS NOT NULL AND month IS NOT NULL
