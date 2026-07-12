-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("crate_id" AS BIGINT) AS crate_id,
    "num",
    CAST("downloads" AS BIGINT) AS downloads,
    CAST("crate_size" AS BIGINT) AS crate_size,
    "license",
    CAST("created_at" AS TIMESTAMP) AS created_at,
    "yanked"
FROM "crates-io-versions"
