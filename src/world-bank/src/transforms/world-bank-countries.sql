SELECT
    id                  AS country_code,
    iso2_code,
    name,
    region_id,
    NULLIF(region_value, '')        AS region,
    NULLIF(income_level_value, '')  AS income_level,
    NULLIF(lending_type_value, '')  AS lending_type,
    NULLIF(capital_city, '')        AS capital_city,
    longitude,
    latitude
FROM "world-bank-countries"
WHERE id IS NOT NULL
