-- fao-mddw: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("survey_code" AS BIGINT)           AS survey_code,
    "survey"                                AS survey,
    "food_group_code"                       AS food_group_code,
    "food_group"                            AS food_group,
    CAST("indicator_code" AS BIGINT)        AS indicator_code,
    "indicator"                             AS indicator,
    CAST("geographic_level_code" AS BIGINT) AS geographic_level_code,
    "geographic_level"                      AS geographic_level,
    CAST("element_code" AS BIGINT)          AS element_code,
    "element"                               AS element,
    "unit"                                  AS unit,
    CAST("value" AS DOUBLE)                 AS value,
    "flag"                                  AS flag
FROM "fao-mddw"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
