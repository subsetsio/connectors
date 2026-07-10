-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("id" AS BIGINT) AS id,
    CAST("commodity__sid" AS BIGINT) AS commodity_sid,
    "commodity__code" AS commodity_code,
    CAST("commodity__indent" AS BIGINT) AS commodity_indent,
    "commodity__description" AS commodity_description,
    CAST("measure__sid" AS BIGINT) AS measure_sid,
    CAST("measure__type__id" AS BIGINT) AS measure_type_id,
    "measure__type__description" AS measure_type_description,
    "measure__additional_code__code" AS measure_additional_code_code,
    "measure__additional_code__description" AS measure_additional_code_description,
    "measure__duty_expression" AS measure_duty_expression,
    "measure__effective_start_date" AS measure_effective_start_date,
    "measure__effective_end_date" AS measure_effective_end_date,
    "measure__reduction_indicator" AS measure_reduction_indicator,
    "measure__footnotes" AS measure_footnotes,
    "measure__conditions" AS measure_conditions,
    CAST("measure__geographical_area__sid" AS BIGINT) AS measure_geographical_area_sid,
    "measure__geographical_area__id" AS measure_geographical_area_id,
    "measure__geographical_area__description" AS measure_geographical_area_description,
    "measure__excluded_geographical_areas__ids" AS measure_excluded_geographical_areas_ids,
    "measure__excluded_geographical_areas__descriptions" AS measure_excluded_geographical_areas_descriptions,
    "measure__quota__order_number" AS measure_quota_order_number,
    "measure__regulation__id" AS measure_regulation_id,
    "measure__regulation__url" AS measure_regulation_url
FROM "dbt-uk-tariff-2021-01-01--measures-on-declarable-commodities"
