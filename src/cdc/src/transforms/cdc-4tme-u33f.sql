-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Week_Ending" AS week_ending,
    "Demographic Level" AS demographic_level,
    "Comparison Group 1" AS comparison_group_1,
    "Comparison Group 2" AS comparison_group_2,
    CAST("Comparison Group 1 Estimate" AS DOUBLE) AS comparison_group_1_estimate,
    CAST("Comparison Group 2 Estimate" AS DOUBLE) AS comparison_group_2_estimate,
    CAST("Estimate Difference" AS DOUBLE) AS estimate_difference,
    CAST("Difference Estimate Lower 95 CI" AS DOUBLE) AS difference_estimate_lower_95_ci,
    CAST("Difference Estimate Upper 95 CI" AS DOUBLE) AS difference_estimate_upper_95_ci,
    "Significant at 95 pct" AS significant_at_95_pct,
    CAST("Comparison Group 1 Sort Order" AS BIGINT) AS comparison_group_1_sort_order,
    CAST("Comparison Group 2 Sort Order" AS BIGINT) AS comparison_group_2_sort_order,
    "Age Group" AS age_group
FROM "cdc-4tme-u33f"
