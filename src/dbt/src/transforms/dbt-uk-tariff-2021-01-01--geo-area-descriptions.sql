-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("sid" AS BIGINT) AS sid,
    CAST("described_geographicalarea_id" AS BIGINT) AS described_geographicalarea_id,
    "description",
    "validity_start"
FROM "dbt-uk-tariff-2021-01-01--geo-area-descriptions"
