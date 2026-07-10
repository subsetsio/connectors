-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "candidate",
    "date",
    "pct_estimate",
    "state",
    "pct_trend_adjusted",
    "cycle",
    "party"
FROM "fivethirtyeight-polls-old-model-2024-presidential-primary-averages-old-model"
