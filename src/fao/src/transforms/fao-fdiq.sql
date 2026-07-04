-- fao-fdiq: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("survey_code" AS BIGINT)           AS survey_code,
    "survey"                                AS survey,
    CAST("geographic_level_code" AS BIGINT) AS geographic_level_code,
    "geographic_level"                      AS geographic_level,
    "population_age_group_code"             AS population_age_group_code,
    "population_age_group"                  AS population_age_group,
    "food_group_code"                       AS food_group_code,
    "food_group"                            AS food_group,
    CAST("indicator_code" AS BIGINT)        AS indicator_code,
    "indicator"                             AS indicator,
    CAST("element_code" AS BIGINT)          AS element_code,
    "element"                               AS element,
    CAST("sex_code" AS BIGINT)              AS sex_code,
    "sex"                                   AS sex,
    "unit"                                  AS unit,
    CAST("value" AS DOUBLE)                 AS value,
    "flag"                                  AS flag,
    "note"                                  AS note
FROM "fao-fdiq"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
