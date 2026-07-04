-- fao-sxs: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("area_code" AS BIGINT)             AS area_code,
    ltrim("area_code_m49", '''')            AS area_code_m49,
    "area"                                  AS area,
    "item_code"                             AS item_code,
    ltrim("item_code_sdg", '''')            AS item_code_sdg,
    "item"                                  AS item,
    CAST("element_code" AS BIGINT)          AS element_code,
    "element"                               AS element,
    CAST("sex_code" AS BIGINT)              AS sex_code,
    ltrim("sex_code_sdg", '''')             AS sex_code_sdg,
    "sex"                                   AS sex,
    "population_age_group_code"             AS population_age_group_code,
    "population_age_group"                  AS population_age_group,
    CAST("geographic_level_code" AS BIGINT) AS geographic_level_code,
    "geographic_level"                      AS geographic_level,
    CAST("activity_code" AS BIGINT)         AS activity_code,
    ltrim("activity_code_sdg", '''')        AS activity_code_sdg,
    "activity"                              AS activity,
    CAST("year" AS BIGINT)                  AS year,
    "unit"                                  AS unit,
    CAST("value" AS DOUBLE)                 AS value,
    "flag"                                  AS flag,
    "note"                                  AS note
FROM "fao-sxs"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
