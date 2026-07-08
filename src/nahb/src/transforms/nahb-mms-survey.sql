SELECT period, CAST(date AS DATE) AS date, index_type, component,
       CAST(value AS DOUBLE) AS value
FROM "nahb-mms-survey" WHERE value IS NOT NULL
