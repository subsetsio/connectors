-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Vaccine" AS vaccine,
    "demo_group",
    "demo_category",
    "Indicator_group" AS indicator_group,
    "Indicator_category" AS indicator_category,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("Lower_ci" AS DOUBLE) AS lower_ci,
    CAST("Upper_ci" AS DOUBLE) AS upper_ci,
    CAST("Unweighted Sample Size" AS BIGINT) AS unweighted_sample_size,
    "Month_label" AS month_label,
    "Timeframe_survey" AS timeframe_survey,
    "Dashboard_type" AS dashboard_type,
    CAST("Suppression_flag" AS BIGINT) AS suppression_flag,
    "season",
    "trend_month",
    "trend_label"
FROM "cdc-94wp-9pid"
