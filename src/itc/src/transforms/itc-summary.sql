SELECT
    CAST(year AS INTEGER)        AS year,
    CAST(budgets AS DOUBLE)      AS budgets,
    CAST(expenses AS DOUBLE)     AS expenses,
    CAST(funds AS DOUBLE)        AS funds,
    CAST(commitments AS DOUBLE)  AS commitments,
    CAST(activities AS INTEGER)  AS activities,
    CAST(donors AS INTEGER)      AS donors,
    CAST(countries AS INTEGER)   AS countries
FROM "itc-summary"
