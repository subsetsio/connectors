SELECT
    CAST(period AS INTEGER)  AS period,
    country,
    indicator_code,
    indicator_name,
    CAST(value AS DOUBLE)    AS value
FROM "eba-risk-dashboard-kri"
WHERE value IS NOT NULL
