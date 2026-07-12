-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    "name",
    "description",
    CAST("created_at" AS TIMESTAMP) AS created_at,
    CAST("updated_at" AS TIMESTAMP) AS updated_at,
    "homepage",
    "documentation",
    "repository",
    CAST("downloads" AS BIGINT) AS downloads
FROM "crates-io-crates"
