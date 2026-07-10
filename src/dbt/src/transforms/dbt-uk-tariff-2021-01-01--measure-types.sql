-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("trackedmodel_ptr_id" AS BIGINT) AS trackedmodel_ptr_id,
    "sid",
    CAST("measure_type_series_id" AS BIGINT) AS measure_type_series_id,
    CAST("trade_movement_code" AS BIGINT) AS trade_movement_code,
    CAST("priority_code" AS BIGINT) AS priority_code,
    CAST("measure_component_applicability_code" AS BIGINT) AS measure_component_applicability_code,
    CAST("origin_destination_code" AS BIGINT) AS origin_destination_code,
    CAST("order_number_capture_code" AS BIGINT) AS order_number_capture_code,
    CAST("measure_explosion_level" AS BIGINT) AS measure_explosion_level,
    "description",
    "validity_start",
    "validity_end"
FROM "dbt-uk-tariff-2021-01-01--measure-types"
