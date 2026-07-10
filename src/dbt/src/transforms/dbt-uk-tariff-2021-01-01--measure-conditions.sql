-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("sid" AS BIGINT) AS sid,
    CAST("component_sequence_number" AS BIGINT) AS component_sequence_number,
    "duty_amount",
    "action_id",
    CAST("condition_code_id" AS BIGINT) AS condition_code_id,
    "condition_measurement_id",
    CAST("dependent_measure_id" AS BIGINT) AS dependent_measure_id,
    "monetary_unit_id",
    "required_certificate_id"
FROM "dbt-uk-tariff-2021-01-01--measure-conditions"
