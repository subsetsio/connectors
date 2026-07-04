-- fao-ae: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("area_code" AS BIGINT)          AS area_code,
    ltrim("area_code_m49", '''')         AS area_code_m49,
    "area"                               AS area,
    CAST("indicator_code" AS BIGINT)     AS indicator_code,
    "indicator"                          AS indicator,
    CAST("cost_category_code" AS BIGINT) AS cost_category_code,
    "cost_category"                      AS cost_category,
    CAST("institution_code" AS BIGINT)   AS institution_code,
    "institution"                        AS institution,
    CAST("year" AS BIGINT)               AS year,
    "unit"                               AS unit,
    CAST("value" AS DOUBLE)              AS value,
    "flag"                               AS flag
FROM "fao-ae"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
