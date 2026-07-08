SELECT
    CAST(year AS INTEGER)     AS year,
    code,
    name,
    kind,
    region_code,
    CAST(lat AS DOUBLE)       AS latitude,
    CAST(lon AS DOUBLE)       AS longitude,
    CAST(budgets AS DOUBLE)   AS budgets,
    CAST(expenses AS DOUBLE)  AS expenses,
    CAST(activities AS INTEGER) AS activities
FROM "itc-map"
WHERE code IS NOT NULL
