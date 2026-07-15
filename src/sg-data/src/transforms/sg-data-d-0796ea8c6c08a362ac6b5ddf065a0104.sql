-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "types_of_inmates",
    "cbp_completion_rate"
FROM "sg-data-d-0796ea8c6c08a362ac6b5ddf065a0104"
