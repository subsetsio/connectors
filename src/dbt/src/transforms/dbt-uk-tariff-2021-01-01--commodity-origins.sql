-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("derived_from_goods_nomenclature_id" AS BIGINT) AS derived_from_goods_nomenclature_id,
    CAST("new_goods_nomenclature_id" AS BIGINT) AS new_goods_nomenclature_id
FROM "dbt-uk-tariff-2021-01-01--commodity-origins"
