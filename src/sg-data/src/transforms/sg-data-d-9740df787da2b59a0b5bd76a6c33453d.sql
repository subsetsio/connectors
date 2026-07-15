-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "waste_type",
    "recycling_rate"
FROM "sg-data-d-9740df787da2b59a0b5bd76a6c33453d"
