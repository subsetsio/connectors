-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Geography_name" AS geography_name,
    "Geography_level" AS geography_level,
    "Demographic_Level" AS demographic_level,
    "Demographic_Name" AS demographic_name,
    "Curr_season" AS curr_season,
    "Past_season" AS past_season,
    CAST("past_week_ending" AS TIMESTAMP) AS past_week_ending,
    "Season_filter_text" AS season_filter_text,
    CAST("Curr_est" AS DOUBLE) AS curr_est,
    "Current_season_Week_Ending" AS current_season_week_ending,
    CAST("Past_est" AS DOUBLE) AS past_est,
    CAST("Curr_CI_HalfWidth" AS DOUBLE) AS curr_ci_halfwidth,
    CAST("Past_CI_HalfWidth" AS DOUBLE) AS past_ci_halfwidth,
    CAST("Difference_estimate" AS DOUBLE) AS difference_estimate,
    CAST("Significance" AS DOUBLE) AS significance,
    "Curr_CI_95" AS curr_ci_95,
    "Past_CI_95" AS past_ci_95,
    "diff_CI_95" AS diff_ci_95,
    "Difference_indicator" AS difference_indicator,
    CAST("Difference_legend_sort" AS BIGINT) AS difference_legend_sort,
    "BinRangeText" AS binrangetext,
    CAST("BinRangeOrder" AS BIGINT) AS binrangeorder,
    CAST("Geography_name_order" AS BIGINT) AS geography_name_order
FROM "cdc-eanj-9nie"
