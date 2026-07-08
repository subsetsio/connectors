SELECT period, CAST(date AS DATE) AS date, metric, segment, geography,
       CAST(value AS DOUBLE) AS value
FROM "nahb-hbgi-full-findings" WHERE value IS NOT NULL
