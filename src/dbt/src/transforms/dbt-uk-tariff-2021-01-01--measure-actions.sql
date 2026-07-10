-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    "code",
    "description",
    CAST("requires_duty" AS BIGINT) AS requires_duty,
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--measure-actions"
