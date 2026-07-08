SELECT CAST(date AS DATE) AS date, country, sector,
       CAST(value AS DOUBLE) AS demand_twh_dev
FROM "bruegel-european-natural-gas-demand-tracker" WHERE value IS NOT NULL
