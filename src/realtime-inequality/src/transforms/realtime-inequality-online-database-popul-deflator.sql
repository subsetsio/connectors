SELECT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    CAST(year AS INTEGER)  AS year,
    CAST(month AS INTEGER) AS month,
    CAST(pop_adults AS DOUBLE)       AS pop_adults,
    CAST(pop_households AS DOUBLE)   AS pop_households,
    CAST(pop_working_age AS DOUBLE)  AS pop_working_age,
    CAST(deflator AS DOUBLE)         AS deflator
FROM "realtime-inequality-online-database-popul-deflator"
WHERE year IS NOT NULL AND month IS NOT NULL
