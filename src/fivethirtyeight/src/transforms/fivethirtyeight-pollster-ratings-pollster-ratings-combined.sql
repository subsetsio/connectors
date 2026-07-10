-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "pollster",
    "pollster_rating_id",
    "aapor_roper",
    "inactive",
    "numeric_grade",
    "rank",
    "POLLSCORE" AS pollscore,
    "wtd_avg_transparency",
    "number_polls_pollster_total",
    "percent_partisan_work",
    "error_ppm",
    "bias_ppm",
    "number_polls_pollster_time_weighted"
FROM "fivethirtyeight-pollster-ratings-pollster-ratings-combined"
