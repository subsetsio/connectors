SELECT CAST(year AS INTEGER) AS year, country, indicator, breakdown,
       CAST(value AS DOUBLE) AS value
FROM "bruegel-eu-labour-market-outlook-dashboard" WHERE value IS NOT NULL
