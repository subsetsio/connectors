SELECT country_id, country_iso3_code, product_id,
       product_sitc_code AS product_code, product_level, year,
       export_value, import_value, global_market_share,
       distance, cog, pci
FROM "harvard-growth-lab-atlas-of-economic-complexity-sitc-country-product-year" WHERE year IS NOT NULL
