-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("additional_code_type_id" AS BIGINT) AS additional_code_type_id,
    CAST("measure_type_id" AS BIGINT) AS measure_type_id,
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--measure-additional-code-types"
