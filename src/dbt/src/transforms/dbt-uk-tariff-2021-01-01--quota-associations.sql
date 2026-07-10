-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("main_quota_id" AS BIGINT) AS main_quota_id,
    CAST("sub_quota_id" AS BIGINT) AS sub_quota_id,
    "sub_quota_relation_type",
    CAST("coefficient" AS DOUBLE) AS coefficient
FROM "dbt-uk-tariff-2021-01-01--quota-associations"
