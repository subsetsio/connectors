SELECT product_id, product_hs22_code AS product_code, product_level, year,
       export_value, import_value, pci
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs22-product-year" WHERE year IS NOT NULL
