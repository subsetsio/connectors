-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geographic Level" AS geographic_level,
    "Geographic Name" AS geographic_name,
    "Demographic_Level" AS demographic_level,
    "Demographic Name" AS demographic_name,
    "Indicator_label" AS indicator_label,
    "Indicator_category_label" AS indicator_category_label,
    "Month_Week" AS month_week,
    CAST("Week_ending" AS TIMESTAMP) AS week_ending,
    CAST("Current_Season_Week_Ending_Label" AS TIMESTAMP) AS current_season_week_ending_label,
    CAST("Estimate" AS DOUBLE) AS estimate,
    CAST("CI_Half_width_95pct" AS DOUBLE) AS ci_half_width_95pct,
    CAST("Unweighted Sample Size" AS BIGINT) AS unweighted_sample_size,
    CAST("Weighted Sample Size" AS BIGINT) AS weighted_sample_size,
    "Legend_Label" AS legend_label,
    CAST("Indicator_Category_Label_Sort" AS BIGINT) AS indicator_category_label_sort,
    CAST("Demographic_Level_Sort_Order" AS BIGINT) AS demographic_level_sort_order,
    CAST("Geography_name_order" AS BIGINT) AS geography_name_order,
    CAST("Geography_Level_Sort_Order" AS BIGINT) AS geography_level_sort_order,
    CAST("Season_Sort" AS BIGINT) AS season_sort,
    CAST("Legend_Sort" AS BIGINT) AS legend_sort,
    CAST("suppression_flag" AS BIGINT) AS suppression_flag,
    "influenza_season"
FROM "cdc-judz-8etw"
