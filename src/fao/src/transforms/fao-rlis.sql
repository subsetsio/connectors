-- fao-rlis: typed long-format FAOSTAT Normalized dump.
-- Rows whose value is empty or non-numeric (flag-only or censored) are dropped.
SELECT
    CAST("survey_code" AS BIGINT)    AS survey_code,
    "survey"                         AS survey,
    CAST("indicator_code" AS BIGINT) AS indicator_code,
    "indicator"                      AS indicator,
    CAST("element_code" AS BIGINT)   AS element_code,
    "element"                        AS element,
    "qualifier_code"                 AS qualifier_code,
    "qualifier"                      AS qualifier,
    CAST("source_code" AS BIGINT)    AS source_code,
    "source"                         AS source,
    "unit"                           AS unit,
    CAST("value" AS DOUBLE)          AS value,
    "flag"                           AS flag,
    "note"                           AS note
FROM "fao-rlis"
WHERE TRY_CAST("value" AS DOUBLE) IS NOT NULL
