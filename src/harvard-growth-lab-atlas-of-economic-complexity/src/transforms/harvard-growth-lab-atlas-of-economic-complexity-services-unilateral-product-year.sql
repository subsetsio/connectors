SELECT product_id, product_services_unilateral_code AS product_code, product_level, year,
       export_value, import_value, pci
FROM "harvard-growth-lab-atlas-of-economic-complexity-services-unilateral-product-year" WHERE year IS NOT NULL
