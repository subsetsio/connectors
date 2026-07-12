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
    "organization_city",
    CAST("organization_zip" AS BIGINT) AS organization_zip,
    "service_description",
    "service_method_name",
    CAST("median_allowed_amt" AS DOUBLE) AS median_allowed_amt,
    CAST("lower_25_allowed_amt" AS DOUBLE) AS lower_25_allowed_amt,
    CAST("upper_75_allowed_amt" AS DOUBLE) AS upper_75_allowed_amt,
    CAST("reporting_period_begin_dt" AS TIMESTAMP) AS reporting_period_begin_dt,
    CAST("reporting_period_end_dt" AS TIMESTAMP) AS reporting_period_end_dt
FROM "washington-ofm-socrata-tw6a-23eg"
