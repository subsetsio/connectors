-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("sid" AS BIGINT) AS sid,
    CAST("order_number_id" AS BIGINT) AS order_number_id,
    CAST("geographical_area_id" AS BIGINT) AS geographical_area_id,
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--quota-origins"
