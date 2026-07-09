SELECT country_id, country_iso3_code, product_id,
       product_services_unilateral_code AS product_code, product_level, year,
       export_value, import_value, global_market_share
FROM "harvard-growth-lab-atlas-of-economic-complexity-services-unilateral-country-product-year" WHERE year IS NOT NULL
