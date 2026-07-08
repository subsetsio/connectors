SELECT CAST(year AS INTEGER)  AS year,
       CAST(month AS INTEGER) AS month,
       make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 15) AS date,
       CAST(fill_flag AS INTEGER) AS fill_flag,
       CAST(mlo AS DOUBLE)     AS mlo,
       CAST(spo AS DOUBLE)     AS spo,
       CAST(average AS DOUBLE) AS average
FROM "scripps-co2-mlo-spo-monthly-mean"
WHERE average IS NOT NULL
