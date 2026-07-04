-- fao-oer: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("area_code" AS BIGINT)      AS area_code,
    ltrim("area_code_m49", '''')     AS area_code_m49,
    "area"                           AS area,
    CAST("source_code" AS BIGINT)    AS source_code,
    "source"                         AS source,
    CAST("indicator_code" AS BIGINT) AS indicator_code,
    "indicator"                      AS indicator,
    CAST("sex_code" AS BIGINT)       AS sex_code,
    "sex"                            AS sex,
    CAST("element_code" AS BIGINT)   AS element_code,
    "element"                        AS element,
    CAST("year" AS BIGINT)           AS year,
    "unit"                           AS unit,
    CAST("value" AS DOUBLE)          AS value,
    "flag"                           AS flag,
    "note"                           AS note
FROM "fao-oer"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
