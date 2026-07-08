SELECT CAST(date AS DATE) AS date, country, holder_type, frequency,
       CAST(value AS DOUBLE) AS value
FROM "bruegel-sovereign-bond-holdings" WHERE value IS NOT NULL
