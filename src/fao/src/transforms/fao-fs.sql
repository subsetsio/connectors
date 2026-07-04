-- fao-fs: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("area_code" AS BIGINT)          AS area_code,
    ltrim("area_code_m49", '''')         AS area_code_m49,
    "area"                               AS area,
    "item_code"                          AS item_code,
    "item"                               AS item,
    CAST("element_code" AS BIGINT)       AS element_code,
    "element"                            AS element,
    "year"                               AS year,
    CAST(substr("year", 1, 4) AS BIGINT) AS year_start,
    CAST(right("year", 4) AS BIGINT)     AS year_end,
    "unit"                               AS unit,
    CAST("value" AS DOUBLE)              AS value,
    "flag"                               AS flag,
    "note"                               AS note
FROM "fao-fs"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
