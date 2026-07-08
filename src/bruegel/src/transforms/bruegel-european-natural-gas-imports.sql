SELECT CAST(date AS DATE) AS date, source,
       CAST(flow_gwh_d AS DOUBLE) AS flow_gwh_d
FROM "bruegel-european-natural-gas-imports" WHERE flow_gwh_d IS NOT NULL
