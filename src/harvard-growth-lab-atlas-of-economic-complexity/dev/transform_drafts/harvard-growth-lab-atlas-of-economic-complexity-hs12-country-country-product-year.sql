SELECT country_id, country_iso3_code,
       partner_country_id, partner_iso3_code,
       product_id, product_hs12_code AS product_code, year,
       export_value, import_value
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs12-country-country-product-year" WHERE year IS NOT NULL
