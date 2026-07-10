-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine" AS vaccine,
    "Age Group" AS age_group,
    "Geography_level" AS geography_level,
    "Geography_name" AS geography_name,
    "Demographic Level" AS demographic_level,
    "Demographic Name" AS demographic_name,
    "Indicator_label" AS indicator_label,
    "Indicator_category_label" AS indicator_category_label,
    "Month_Week" AS month_week,
    "Week_ending" AS week_ending,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("CI_Half_width_95pct" AS DOUBLE) AS ci_half_width_95pct,
    CAST("Unweighted Sample Size" AS BIGINT) AS unweighted_sample_size,
    CAST("Suppresion_flag" AS BIGINT) AS suppresion_flag
FROM "cdc-qeq7-f3ir"
