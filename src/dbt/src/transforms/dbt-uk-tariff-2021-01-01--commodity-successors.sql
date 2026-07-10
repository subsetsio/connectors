-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("absorbed_into_goods_nomenclature_id" AS BIGINT) AS absorbed_into_goods_nomenclature_id,
    CAST("replaced_goods_nomenclature_id" AS BIGINT) AS replaced_goods_nomenclature_id
FROM "dbt-uk-tariff-2021-01-01--commodity-successors"
