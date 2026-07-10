-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "vaccine",
    "influenza_season",
    "geographic_level",
    "geographic_name",
    "demographic_level",
    "demographic_name",
    "indicator_label",
    "indicator_category_label",
    "month_week",
    strptime("week_ending", '%Y-%m-%d')::DATE AS week_ending,
    CAST("nd_weekly_estimate" AS DOUBLE) AS nd_weekly_estimate,
    CAST("ci_half_width_90pct" AS DOUBLE) AS ci_half_width_90pct,
    CAST("ci_half_width_95pct" AS DOUBLE) AS ci_half_width_95pct,
    "n_weighted",
    CAST("n_unweighted" AS BIGINT) AS n_unweighted,
    CAST("suppression_flag" AS BIGINT) AS suppression_flag,
    "data_source"
FROM "cdc-5c6r-xi2t"
