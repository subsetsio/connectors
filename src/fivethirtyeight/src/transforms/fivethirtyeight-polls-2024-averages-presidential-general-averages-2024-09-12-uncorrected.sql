-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "candidate",
    "date",
    "pct_trend_adjusted",
    "state",
    "cycle",
    "party",
    "pct_estimate",
    "hi",
    "lo"
FROM "fivethirtyeight-polls-2024-averages-presidential-general-averages-2024-09-12-uncorrected"
