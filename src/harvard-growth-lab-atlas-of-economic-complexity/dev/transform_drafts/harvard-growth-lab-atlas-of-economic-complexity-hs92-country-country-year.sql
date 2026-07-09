SELECT country_id, country_iso3_code,
       partner_country_id, partner_iso3_code, year,
       export_value, import_value
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs92-country-country-year" WHERE year IS NOT NULL
