-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "candidate",
    "pct_estimate",
    "lo",
    "hi",
    "date",
    "election",
    "cycle"
FROM "fivethirtyeight-polls-old-model-generic-ballot-averages-old-model"
