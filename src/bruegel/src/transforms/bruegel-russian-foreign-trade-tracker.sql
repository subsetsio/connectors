SELECT figure, CAST(date AS DATE) AS date, direction_of_trade,
       country, unit, sitc_code, sitc_category,
       CAST(value AS DOUBLE) AS value
FROM "bruegel-russian-foreign-trade-tracker" WHERE value IS NOT NULL
