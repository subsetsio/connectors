-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "politician",
    "response",
    "date",
    "pct_estimate"
FROM "fivethirtyeight-polls-old-model-nikki-haley-favorability-old-model"
