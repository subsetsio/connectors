SELECT CAST(soc AS VARCHAR) AS soc, occupation_title,
       CAST(employment AS BIGINT) AS employment,
       CAST(mean_wage AS DOUBLE) AS mean_wage,
       CAST(pct10 AS DOUBLE) AS pct10, CAST(pct25 AS DOUBLE) AS pct25,
       CAST(median_wage AS DOUBLE) AS median_wage,
       CAST(pct75 AS DOUBLE) AS pct75, CAST(pct90 AS DOUBLE) AS pct90,
       CAST(mean_wage_rse AS DOUBLE) AS mean_wage_rse,
       CAST(employment_rse AS DOUBLE) AS employment_rse
FROM "alaska-department-of-labor-and-workforce-development-wages-by-occupation"
WHERE occupation_title IS NOT NULL
