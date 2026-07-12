-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("crate_id" AS BIGINT) AS crate_id,
    CAST("category_id" AS BIGINT) AS category_id
FROM "crates-io-crate-categories"
