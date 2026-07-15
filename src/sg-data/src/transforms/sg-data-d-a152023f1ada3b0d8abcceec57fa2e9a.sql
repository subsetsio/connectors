-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "employment_size",
    "computer_usage"
FROM "sg-data-d-a152023f1ada3b0d8abcceec57fa2e9a"
