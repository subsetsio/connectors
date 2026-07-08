SELECT product_id, product_hs92_code AS product_code, product_level, year,
       export_value, import_value, pci
FROM "harvard-growth-lab-atlas-of-economic-complexity-hs92-product-year" WHERE year IS NOT NULL
