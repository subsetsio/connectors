-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("geo_group_id" AS BIGINT) AS geo_group_id,
    CAST("member_id" AS BIGINT) AS member_id,
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--geo-area-memberships"
