SELECT
    CAST(year AS INTEGER)        AS year,
    CAST(quarter AS INTEGER)     AS quarter,
    TRY_CAST(replace(first_estimate, '%', '') AS DOUBLE)     AS first_estimate_pct,
    TRY_CAST(replace(second_estimate, '%', '') AS DOUBLE)    AS second_estimate_pct,
    TRY_CAST(replace(third_estimate, '%', '') AS DOUBLE)     AS third_estimate_pct,
    TRY_CAST(replace(revised_final, '%', '') AS DOUBLE)      AS revised_final_pct
FROM "american-staffing-association-gdp-quarterly-projections"
WHERE year IS NOT NULL AND quarter IS NOT NULL
