-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("sid" AS BIGINT) AS sid,
    CAST("order_number_id" AS BIGINT) AS order_number_id,
    "volume",
    "initial_volume",
    CAST("maximum_precision" AS BIGINT) AS maximum_precision,
    CAST("quota_critical" AS BIGINT) AS quota_critical,
    CAST("quota_critical_threshold" AS BIGINT) AS quota_critical_threshold,
    "description",
    "measurement_unit_id",
    "measurement_unit_qualifier_id",
    "monetary_unit_id",
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--quota-definitions"
