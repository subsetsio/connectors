-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "keyword",
    CAST("crates_cnt" AS BIGINT) AS crates_cnt,
    CAST("created_at" AS TIMESTAMP) AS created_at
FROM "crates-io-keywords"
