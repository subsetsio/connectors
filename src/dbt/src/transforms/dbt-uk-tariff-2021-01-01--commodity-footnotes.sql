-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("goods_nomenclature_id" AS BIGINT) AS goods_nomenclature_id,
    CAST("associated_footnote_id" AS BIGINT) AS associated_footnote_id,
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--commodity-footnotes"
