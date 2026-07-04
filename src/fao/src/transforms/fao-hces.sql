-- fao-hces: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("survey_code" AS BIGINT)           AS survey_code,
    "survey"                                AS survey,
    CAST("geographic_level_code" AS BIGINT) AS geographic_level_code,
    "geographic_level"                      AS geographic_level,
    "food_group_code"                       AS food_group_code,
    "food_group"                            AS food_group,
    CAST("indicator_code" AS BIGINT)        AS indicator_code,
    "indicator"                             AS indicator,
    "element_code"                          AS element_code,
    "element"                               AS element,
    "unit"                                  AS unit,
    CAST("value" AS DOUBLE)                 AS value,
    "flag"                                  AS flag,
    "note"                                  AS note
FROM "fao-hces"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
