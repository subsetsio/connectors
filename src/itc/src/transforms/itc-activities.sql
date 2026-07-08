SELECT
    identifier,
    title,
    description,
    scope,
    status,
    reporting_org_name,
    CAST(planned_end AS DATE)        AS planned_end,
    CAST(actual_start AS DATE)       AS actual_start,
    CAST(total_budget AS DOUBLE)     AS total_budget,
    CAST(total_expense AS DOUBLE)    AS total_expense,
    CAST(date_first_expense AS DATE) AS date_first_expense,
    CAST(date_last_expense AS DATE)  AS date_last_expense
FROM "itc-activities"
WHERE identifier IS NOT NULL
