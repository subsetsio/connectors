-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vaccine",
    "geographic_level",
    "geographic_name",
    "Demographic_level" AS demographic_level,
    "Demographic_name" AS demographic_name,
    "Indicator_label" AS indicator_label,
    "month_week",
    CAST("curr_week_ending" AS TIMESTAMP) AS curr_week_ending,
    CAST("Previous_week_ending" AS TIMESTAMP) AS previous_week_ending,
    "curr_season",
    "Past_season" AS past_season,
    CAST("curr_est" AS DOUBLE) AS curr_est,
    CAST("past_est" AS DOUBLE) AS past_est,
    CAST("Curr_ci_halfwidth_95pct" AS DOUBLE) AS curr_ci_halfwidth_95pct,
    CAST("Past_ci_halfwidth_95pct" AS DOUBLE) AS past_ci_halfwidth_95pct,
    CAST("difference_estimate" AS DOUBLE) AS difference_estimate,
    CAST("significance" AS DOUBLE) AS significance,
    "curr_ci_95",
    "past_ci_95",
    "diff_ci_95",
    "difference_indicator",
    CAST("estimate" AS DOUBLE) AS estimate,
    "binrangetext",
    CAST("binrangeorder" AS BIGINT) AS binrangeorder
FROM "cdc-n97r-u9uh"
