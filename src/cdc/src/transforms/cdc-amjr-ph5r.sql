-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "comparison_type",
    CAST("week_ending" AS TIMESTAMP) AS week_ending,
    CAST("current_season_week_ending_label" AS TIMESTAMP) AS current_season_week_ending_label,
    "comparison_group_1",
    "comparison_group_2",
    CAST("comparison_group1_point_estimate" AS DOUBLE) AS comparison_group1_point_estimate,
    CAST("comparison_group2_point_estimate" AS DOUBLE) AS comparison_group2_point_estimate,
    CAST("estimate_difference" AS DOUBLE) AS estimate_difference,
    CAST("difference_estimate_lower_95_ci" AS DOUBLE) AS difference_estimate_lower_95_ci,
    CAST("difference_estimate_upper_95_ci" AS DOUBLE) AS difference_estimate_upper_95_ci,
    "significant_at_95_pct",
    CAST("comparison_group_1_sort_order" AS BIGINT) AS comparison_group_1_sort_order,
    CAST("comparison_group_2_sort_order" AS BIGINT) AS comparison_group_2_sort_order
FROM "cdc-amjr-ph5r"
