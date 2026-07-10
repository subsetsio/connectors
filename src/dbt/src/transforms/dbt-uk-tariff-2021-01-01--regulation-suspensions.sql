-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("enacting_regulation_id" AS BIGINT) AS enacting_regulation_id,
    CAST("target_regulation_id" AS BIGINT) AS target_regulation_id,
    "effective_end_date"
FROM "dbt-uk-tariff-2021-01-01--regulation-suspensions"
