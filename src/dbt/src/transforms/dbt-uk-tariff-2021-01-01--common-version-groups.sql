-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("created_at" AS TIMESTAMP) AS created_at,
    CAST("updated_at" AS TIMESTAMP) AS updated_at,
    "current_version_id"
FROM "dbt-uk-tariff-2021-01-01--common-version-groups"
