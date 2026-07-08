SELECT region, category, metric, CAST(value AS DOUBLE) AS value FROM "damodaran-roe" WHERE value IS NOT NULL AND category IS NOT NULL AND metric IS NOT NULL
