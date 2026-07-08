SELECT zone, CAST(year AS INTEGER) AS year, tech,
       CAST(CF AS DOUBLE) AS capacity_factor,
       CAST(MV AS DOUBLE) AS market_value,
       CAST(CV AS DOUBLE) AS capture_value
FROM "bruegel-eu-renewables-value-tracker" WHERE CF IS NOT NULL OR MV IS NOT NULL OR CV IS NOT NULL
