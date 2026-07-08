SELECT country_id, country_iso3_code, product_id,
       product_hs22_code AS product_code, product_level, year,
       export_value, import_value, global_market_share,
       distance, cog, pci
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs22-country-product-year" WHERE year IS NOT NULL
