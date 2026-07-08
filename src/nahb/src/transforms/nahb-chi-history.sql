SELECT period, CAST(date AS DATE) AS date,
       CAST(msa_fip AS INTEGER) AS msa_fip,
       CAST(flag AS INTEGER) AS flag, name,
       CAST(value AS DOUBLE) AS value
FROM "nahb-chi-history" WHERE value IS NOT NULL
