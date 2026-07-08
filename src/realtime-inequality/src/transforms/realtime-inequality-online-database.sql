SELECT
    make_date(CAST(year AS INTEGER), CAST(month AS INTEGER), 1) AS date,
    CAST(year AS INTEGER)  AS year,
    CAST(month AS INTEGER) AS month,
    "group"                AS rank_group,
    unit,
    CAST(pop AS DOUBLE)                          AS pop,
    CAST(factor_income AS DOUBLE)                AS factor_income,
    CAST(pretax_income AS DOUBLE)                AS pretax_income,
    CAST(posttax_income AS DOUBLE)               AS posttax_income,
    CAST(disposable_income AS DOUBLE)            AS disposable_income,
    CAST(wealth AS DOUBLE)                       AS wealth,
    CAST(threshold_factor_income AS DOUBLE)      AS threshold_factor_income,
    CAST(threshold_pretax_income AS DOUBLE)      AS threshold_pretax_income,
    CAST(threshold_posttax_income AS DOUBLE)     AS threshold_posttax_income,
    CAST(threshold_disposable_income AS DOUBLE)  AS threshold_disposable_income,
    CAST(threshold_wealth AS DOUBLE)             AS threshold_wealth,
    CAST(deflator AS DOUBLE)                     AS deflator
FROM "realtime-inequality-online-database"
WHERE year IS NOT NULL AND month IS NOT NULL AND "group" IS NOT NULL
