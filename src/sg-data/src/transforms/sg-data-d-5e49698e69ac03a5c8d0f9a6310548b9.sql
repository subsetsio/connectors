-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "product_segment",
    "total_allocated",
    "supply"
FROM "sg-data-d-5e49698e69ac03a5c8d0f9a6310548b9"
