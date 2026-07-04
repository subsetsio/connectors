-- fao-gfdi: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("area_code" AS BIGINT)       AS area_code,
    ltrim("area_code_m49", '''')      AS area_code_m49,
    "area"                            AS area,
    CAST("food_value_code" AS BIGINT) AS food_value_code,
    "food_value"                      AS food_value,
    CAST("industry_code" AS BIGINT)   AS industry_code,
    "industry"                        AS industry,
    CAST("factor_code" AS BIGINT)     AS factor_code,
    "factor"                          AS factor,
    CAST("element_code" AS BIGINT)    AS element_code,
    "element"                         AS element,
    CAST("year" AS BIGINT)            AS year,
    "unit"                            AS unit,
    CAST("value" AS DOUBLE)           AS value,
    "flag"                            AS flag
FROM "fao-gfdi"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
