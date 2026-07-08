SELECT CAST(date AS DATE) AS date, commodity, unit, seasonal_adj,
       flow, partner, CAST(value AS DOUBLE) AS value
FROM "bruegel-global-trade-tracker" WHERE value IS NOT NULL
