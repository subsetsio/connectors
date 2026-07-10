-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("modified_measure_id" AS BIGINT) AS modified_measure_id,
    CAST("excluded_geographical_area_id" AS BIGINT) AS excluded_geographical_area_id
FROM "dbt-uk-tariff-2021-01-01--measure-excluded-geo-areas"
