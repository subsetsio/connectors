SELECT
    identifier,
    CAST(year AS INTEGER)   AS year,
    CAST(budget AS DOUBLE)  AS budget,
    CAST(expense AS DOUBLE) AS expense
FROM "itc-activity-financials"
WHERE identifier IS NOT NULL AND year IS NOT NULL
