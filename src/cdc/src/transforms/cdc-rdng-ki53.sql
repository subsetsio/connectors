-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geography_Name" AS geography_name,
    "Geographic Level" AS geographic_level,
    "Comparison_Type" AS comparison_type,
    CAST("Month_Week" AS TIMESTAMP) AS month_week,
    "Curr_season" AS curr_season,
    "Past_season" AS past_season,
    "Current_Season_Week_Ending_Date" AS current_season_week_ending_date,
    CAST("Past_Season_Week_Ending_Date" AS TIMESTAMP) AS past_season_week_ending_date,
    "Season_filter_text" AS season_filter_text,
    CAST("Curr_estimate" AS DOUBLE) AS curr_estimate,
    CAST("Past_estimate" AS DOUBLE) AS past_estimate,
    CAST("Curr_CI_HalfWidth" AS DOUBLE) AS curr_ci_halfwidth,
    CAST("Past_CI_HalfWidth" AS DOUBLE) AS past_ci_halfwidth,
    CAST("Estimate_Difference" AS DOUBLE) AS estimate_difference,
    CAST("Significance" AS DOUBLE) AS significance,
    "Curr_CI_95" AS curr_ci_95,
    "Diff_CI_95" AS diff_ci_95,
    "Difference_indicator" AS difference_indicator,
    CAST("Difference_legend_sort" AS BIGINT) AS difference_legend_sort,
    "BinRangeText" AS binrangetext,
    CAST("BinRangeOrder" AS BIGINT) AS binrangeorder,
    CAST("Geography_name_order" AS BIGINT) AS geography_name_order
FROM "cdc-rdng-ki53"
