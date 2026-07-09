SELECT country_id, country_iso3_code, year,
       export_value, import_value,
       eci, coi, diversity, growth_proj
FROM "harvard-growth-lab-atlas-of-economic-complexity-sitc-country-year" WHERE year IS NOT NULL
