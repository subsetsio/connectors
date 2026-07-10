-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "race",
    "state",
    "modeldate",
    "candidate_name",
    "candidate_id",
    "pct_estimate",
    "pct_trend_adjusted",
    "timestamp",
    "comment",
    "contestdate"
FROM "fivethirtyeight-polls-pres-primary-avgs-1980-2016"
