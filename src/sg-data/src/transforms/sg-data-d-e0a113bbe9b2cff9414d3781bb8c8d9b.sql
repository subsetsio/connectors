-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "year",
    "retrench_term_contract"
FROM "sg-data-d-e0a113bbe9b2cff9414d3781bb8c8d9b"
