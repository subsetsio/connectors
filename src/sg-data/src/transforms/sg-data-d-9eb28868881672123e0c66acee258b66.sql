-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "occupation1",
    "reentry_rate_12mth"
FROM "sg-data-d-9eb28868881672123e0c66acee258b66"
