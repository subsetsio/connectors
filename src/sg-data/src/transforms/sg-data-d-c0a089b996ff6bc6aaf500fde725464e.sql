-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "course",
    "participant_category",
    "fee_per_term"
FROM "sg-data-d-c0a089b996ff6bc6aaf500fde725464e"
