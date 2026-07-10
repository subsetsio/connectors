-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("update_type" AS BIGINT) AS update_type,
    CAST("polymorphic_ctype_id" AS BIGINT) AS polymorphic_ctype_id,
    CAST("transaction_id" AS BIGINT) AS transaction_id,
    CAST("version_group_id" AS BIGINT) AS version_group_id
FROM "dbt-uk-tariff-2021-01-01--common-tracked-models"
