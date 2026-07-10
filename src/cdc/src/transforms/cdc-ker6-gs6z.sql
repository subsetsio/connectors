-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vaccine",
    "Geographic_Level" AS geographic_level,
    "Geographic_Name" AS geographic_name,
    "Demographic_Level" AS demographic_level,
    "Demographic_Name" AS demographic_name,
    "Indicator_label" AS indicator_label,
    "Indicator_category_label" AS indicator_category_label,
    "Month_Week" AS month_week,
    "Week_ending" AS week_ending,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("CI_Half_width_95pct" AS DOUBLE) AS ci_half_width_95pct,
    CAST("Unweighted_Sample_Size" AS BIGINT) AS unweighted_sample_size,
    CAST("suppression_flag" AS BIGINT) AS suppression_flag
FROM "cdc-ker6-gs6z"
