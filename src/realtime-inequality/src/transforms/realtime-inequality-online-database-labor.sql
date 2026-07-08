SELECT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    CAST(year AS INTEGER)  AS year,
    CAST(month AS INTEGER) AS month,
    "group"                AS rank_group,
    unit,
    CAST(pop AS DOUBLE)                     AS pop,
    CAST(labor_income AS DOUBLE)            AS labor_income,
    CAST(threshold_labor_income AS DOUBLE)  AS threshold_labor_income,
    CAST(wage AS DOUBLE)                    AS wage
FROM "realtime-inequality-online-database-labor"
WHERE year IS NOT NULL AND month IS NOT NULL AND "group" IS NOT NULL
