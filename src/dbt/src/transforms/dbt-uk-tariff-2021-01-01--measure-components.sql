-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("component_measure_id" AS BIGINT) AS component_measure_id,
    "component_measurement_id",
    CAST("duty_expression_id" AS BIGINT) AS duty_expression_id,
    "duty_amount",
    "monetary_unit_id"
FROM "dbt-uk-tariff-2021-01-01--measure-components"
