SELECT
    CAST(year AS INTEGER)        AS year,
    CAST(quarter AS INTEGER)     AS quarter,
    TRY_CAST(replace(replace(replace(trim(sales), '$', ''), ',', ''), ' ', '') AS DOUBLE)              AS sales,
    TRY_CAST(replace(sales_qoq, '%', '') AS DOUBLE)          AS sales_qoq_pct,
    TRY_CAST(replace(sales_yoy, '%', '') AS DOUBLE)          AS sales_yoy_pct,
    TRY_CAST(replace(replace(replace(trim(payroll), '$', ''), ',', ''), ' ', '') AS DOUBLE)            AS payroll,
    TRY_CAST(replace(payroll_qoq, '%', '') AS DOUBLE)        AS payroll_qoq_pct,
    TRY_CAST(replace(payroll_yoy, '%', '') AS DOUBLE)        AS payroll_yoy_pct,
    TRY_CAST(replace(replace(replace(trim(awe), '$', ''), ',', ''), ' ', '') AS DOUBLE)                AS awe,
    TRY_CAST(replace(awe_qoq, '%', '') AS DOUBLE)            AS awe_qoq_pct,
    TRY_CAST(replace(awe_yoy, '%', '') AS DOUBLE)            AS awe_yoy_pct
FROM "american-staffing-association-quarterly-employment-sales"
WHERE year IS NOT NULL AND quarter IS NOT NULL
