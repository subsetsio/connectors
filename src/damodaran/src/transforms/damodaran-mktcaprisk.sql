SELECT category, metric, CAST(value AS DOUBLE) AS value FROM "damodaran-mktcaprisk" WHERE value IS NOT NULL AND category IS NOT NULL AND metric IS NOT NULL
