-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("sid" AS BIGINT) AS sid,
    "prefix",
    CAST("duty_amount_applicability_code" AS BIGINT) AS duty_amount_applicability_code,
    CAST("measurement_unit_applicability_code" AS BIGINT) AS measurement_unit_applicability_code,
    CAST("monetary_unit_applicability_code" AS BIGINT) AS monetary_unit_applicability_code,
    "description",
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--measure-duty-expressions"
