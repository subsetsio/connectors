-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is variable-level codebook metadata extracted from study DDI XML files; summary statistic columns are source-provided metadata, not independently computed observations.
SELECT
    CAST("study_id" AS BIGINT) AS study_id,
    "surveyid",
    "study_title",
    "var_id",
    "name" AS variable_name,
    "intrvl" AS interval_type,
    CAST("decimals" AS BIGINT) AS decimals,
    "label",
    "format_type",
    CAST("stat_valid" AS BIGINT) AS valid_cases,
    CAST("stat_invalid" AS BIGINT) AS invalid_cases,
    "stat_min" AS min_value,
    "stat_max" AS max_value,
    CAST("stat_mean" AS DOUBLE) AS mean_value,
    CAST("stat_stdev" AS DOUBLE) AS stdev_value
FROM "nisr-variables"
