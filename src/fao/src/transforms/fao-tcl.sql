-- fao-tcl: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("area_code" AS BIGINT)    AS area_code,
    ltrim("area_code_m49", '''')   AS area_code_m49,
    "area"                         AS area,
    CAST("item_code" AS BIGINT)    AS item_code,
    ltrim("item_code_cpc", '''')   AS item_code_cpc,
    "item"                         AS item,
    CAST("element_code" AS BIGINT) AS element_code,
    "element"                      AS element,
    CAST("year" AS BIGINT)         AS year,
    "unit"                         AS unit,
    CAST("value" AS DOUBLE)        AS value,
    "flag"                         AS flag,
    "note"                         AS note
FROM "fao-tcl"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
