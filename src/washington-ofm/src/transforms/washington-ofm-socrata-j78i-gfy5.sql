-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Quality and cost summary rows may mix reporting periods, organizations, measures, and aggregation levels; filter the relevant dimensions before comparing or summing measures.
SELECT
    "_entity_id" AS entity_id,
    "_source_type" AS source_type,
    "_socrata_dataset_id" AS socrata_dataset_id,
    "summarization_level",
    "name",
    "product_type",
    "measure_code",
    "measure_description",
    "measure_component",
    "measure_summary_units",
    "age_stratification",
    CAST("measure_result" AS DOUBLE) AS measure_result,
    CAST("lower_95_ci" AS DOUBLE) AS lower_95_ci,
    CAST("upper_95_ci" AS DOUBLE) AS upper_95_ci,
    CAST("reporting_period_begin_dt" AS TIMESTAMP) AS reporting_period_begin_dt,
    CAST("reporting_period_end_dt" AS TIMESTAMP) AS reporting_period_end_dt
FROM "washington-ofm-socrata-j78i-gfy5"
