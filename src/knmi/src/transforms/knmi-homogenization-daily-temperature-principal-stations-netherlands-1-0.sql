SELECT station, variable,
       CAST(date AS DATE) AS date,
       CAST(original AS DOUBLE) AS original,
       CAST(version1 AS DOUBLE) AS version1,
       CAST(version2 AS DOUBLE) AS version2
FROM "knmi-homogenization-daily-temperature-principal-stations-netherlands-1-0"
WHERE date IS NOT NULL
