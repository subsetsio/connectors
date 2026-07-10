-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Comparison_Type" AS comparison_type,
    "Week_Ending" AS week_ending,
    "Current_Season_Week_Ending_Label" AS current_season_week_ending_label,
    "Comparison_Group_1" AS comparison_group_1,
    "Comparison_Group_2" AS comparison_group_2,
    CAST("Comparison_Group1_Point_Estimate" AS DOUBLE) AS comparison_group1_point_estimate,
    CAST("Comparison_Group2_Point_Estimate" AS DOUBLE) AS comparison_group2_point_estimate,
    CAST("Estimate_Difference" AS DOUBLE) AS estimate_difference,
    CAST("Difference_Estimate_Lower_95_CI" AS DOUBLE) AS difference_estimate_lower_95_ci,
    CAST("Difference_Estimate_Upper_95_CI" AS DOUBLE) AS difference_estimate_upper_95_ci,
    "Significant_at_95_pct" AS significant_at_95_pct,
    CAST("Comparison_Group_1_Sort_Order" AS BIGINT) AS comparison_group_1_sort_order,
    CAST("Comparison_Group_2_Sort_Order" AS BIGINT) AS comparison_group_2_sort_order
FROM "cdc-skkh-jsrk"
