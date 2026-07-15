-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "month",
    "father_race",
    "child_gender",
    "birth_count"
FROM "sg-data-d-50f55922b78f0a9eb7ce877e8604a5c0"
