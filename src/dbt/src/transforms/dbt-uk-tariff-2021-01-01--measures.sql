-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Version-tracked TARIC data: each row is one version of a tracked model (keyed by `trackedmodel_ptr_id`). The same logical entity (its `sid`) recurs across rows with different `validity_start`/`validity_end` ranges — filter by the validity window for a point-in-time view instead of assuming one row per entity.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    CAST("sid" AS BIGINT) AS sid,
    CAST("measure_type_id" AS BIGINT) AS measure_type_id,
    "goods_nomenclature_id",
    "additional_code_id",
    "reduction",
    CAST("stopped" AS BIGINT) AS stopped,
    "export_refund_nomenclature_sid",
    CAST("generating_regulation_id" AS BIGINT) AS generating_regulation_id,
    CAST("geographical_area_id" AS BIGINT) AS geographical_area_id,
    "order_number_id",
    "terminating_regulation_id",
    "dead_additional_code",
    "dead_order_number",
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--measures"
