-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "geographic_name",
    "geographic_level",
    "Month_Week" AS month_week,
    "Current_Season_Week_Ending_Label" AS current_season_week_ending_label,
    "curr_season",
    "past_season",
    "demographic_name",
    "season_filter_text",
    CAST("curr_est" AS DOUBLE) AS curr_est,
    CAST("past_est" AS DOUBLE) AS past_est,
    CAST("Current_Week_Ending_Date" AS TIMESTAMP) AS current_week_ending_date,
    CAST("Previous_Week_Ending_Date" AS TIMESTAMP) AS previous_week_ending_date,
    CAST("curr_CI_HalfWidth" AS DOUBLE) AS curr_ci_halfwidth,
    CAST("past_CI_HalfWidth" AS DOUBLE) AS past_ci_halfwidth,
    CAST("Difference_Estimate" AS DOUBLE) AS difference_estimate,
    CAST("Significance" AS DOUBLE) AS significance,
    "curr_CI_95" AS curr_ci_95,
    "Diff_CI_95" AS diff_ci_95,
    "Difference_indicator" AS difference_indicator,
    CAST("Difference_legend_sort" AS BIGINT) AS difference_legend_sort,
    "BinRangeText" AS binrangetext,
    CAST("BinRangeOrder" AS BIGINT) AS binrangeorder,
    CAST("Geography_name_order" AS BIGINT) AS geography_name_order,
    CAST("demographic_name_sort_order" AS BIGINT) AS demographic_name_sort_order
FROM "cdc-qr63-vqq5"
