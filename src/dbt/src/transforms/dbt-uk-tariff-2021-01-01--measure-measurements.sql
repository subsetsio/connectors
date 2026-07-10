-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("measurement_unit_id" AS BIGINT) AS measurement_unit_id,
    "measurement_unit_qualifier_id",
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--measure-measurements"
