-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "quarter",
    "product_segment",
    "total_allocated",
    "supply"
FROM "sg-data-d-a5738475c4f7a3f72e75bc5b734fd7bc"
