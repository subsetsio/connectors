-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: The `kind` column is an integer dependency type code from crates.io rather than a decoded label.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("version_id" AS BIGINT) AS version_id,
    CAST("crate_id" AS BIGINT) AS crate_id,
    "req",
    CAST("kind" AS BIGINT) AS kind,
    "optional",
    "default_features"
FROM "crates-io-dependencies"
