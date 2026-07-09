SELECT year, exporter, importer,
       commoditycode AS product_code,
       value_final, value_exporter, value_importer
FROM "harvard-growth-lab-atlas-of-economic-complexity-reported-hs92-country-country-product-year" WHERE year IS NOT NULL
