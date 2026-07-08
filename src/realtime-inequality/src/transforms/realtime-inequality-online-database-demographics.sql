SELECT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    CAST(year AS INTEGER)  AS year,
    CAST(month AS INTEGER) AS month,
    demo_type,
    "group"                AS demo_group,
    unit,
    CAST(population AS DOUBLE)         AS population,
    CAST(factor_income AS DOUBLE)      AS factor_income,
    CAST(pretax_income AS DOUBLE)      AS pretax_income,
    CAST(posttax_income AS DOUBLE)     AS posttax_income,
    CAST(disposable_income AS DOUBLE)  AS disposable_income,
    CAST(wealth AS DOUBLE)             AS wealth,
    CAST(labor_income AS DOUBLE)       AS labor_income,
    CAST(deflator AS DOUBLE)           AS deflator
FROM "realtime-inequality-online-database-demographics"
WHERE year IS NOT NULL AND month IS NOT NULL
  AND demo_type IS NOT NULL AND "group" IS NOT NULL
