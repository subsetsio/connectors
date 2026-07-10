-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "politician",
    "date",
    "answer",
    "pct_estimate",
    "lo",
    "hi"
FROM "fivethirtyeight-polls-old-model-joe-biden-approval-old-model"
