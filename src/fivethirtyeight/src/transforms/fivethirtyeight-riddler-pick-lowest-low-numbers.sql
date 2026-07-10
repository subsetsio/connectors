-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "Your Number" AS your_number,
    "Show Your Work" AS show_your_work
FROM "fivethirtyeight-riddler-pick-lowest-low-numbers"
