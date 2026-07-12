-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "namespace",
    "repo",
    "description",
    "repository_type",
    "status",
    "status_description",
    CAST("date_registered" AS TIMESTAMP) AS date_registered,
    CAST("last_updated" AS TIMESTAMP) AS last_updated,
    "storage_size" AS storage_size_bytes,
    "categories"
FROM "docker-hub-official-images"
