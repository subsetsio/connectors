-- fao-pe: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("area_code" AS BIGINT)   AS area_code,
    ltrim("area_code_m49", '''')  AS area_code_m49,
    "area"                        AS area,
    "element_code"                AS element_code,
    "element"                     AS element,
    "iso_currency_code"           AS iso_currency_code,
    "currency"                    AS currency,
    CAST("year" AS BIGINT)        AS year,
    CAST("months_code" AS BIGINT) AS months_code,
    "months"                      AS months,
    CAST("value" AS DOUBLE)       AS value,
    "flag"                        AS flag
FROM "fao-pe"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
