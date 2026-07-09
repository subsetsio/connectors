SELECT country_id, country_iso3_code, year,
       export_value, import_value
FROM "harvard-growth-lab-atlas-of-economic-complexity-services-unilateral-country-year" WHERE year IS NOT NULL
