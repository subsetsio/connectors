-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("sid" AS BIGINT) AS sid,
    CAST("quota_definition_id" AS BIGINT) AS quota_definition_id,
    CAST("blocking_period_type" AS BIGINT) AS blocking_period_type,
    "description",
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--quota-blockings"
