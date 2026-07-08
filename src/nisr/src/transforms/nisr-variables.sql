SELECT
    TRY_CAST(study_id AS BIGINT) AS study_id,
    surveyid,
    study_title,
    var_id,
    name                         AS variable_name,
    label,
    intrvl                       AS interval_type,
    format_type,
    TRY_CAST(decimals AS INTEGER)     AS decimals,
    TRY_CAST(stat_valid AS BIGINT)    AS valid_cases,
    TRY_CAST(stat_invalid AS BIGINT)  AS invalid_cases,
    TRY_CAST(stat_min AS DOUBLE)      AS min_value,
    TRY_CAST(stat_max AS DOUBLE)      AS max_value,
    TRY_CAST(stat_mean AS DOUBLE)     AS mean_value,
    TRY_CAST(stat_stdev AS DOUBLE)    AS stdev_value
FROM "nisr-variables"
WHERE var_id IS NOT NULL
QUALIFY row_number() OVER (PARTITION BY study_id, var_id ORDER BY var_id) = 1
