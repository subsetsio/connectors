-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("quota_definition__sid" AS BIGINT) AS quota_definition_sid,
    "quota__order_number" AS quota_order_number,
    "quota__geographical_areas" AS quota_geographical_areas,
    "quota__headings" AS quota_headings,
    "quota__commodities" AS quota_commodities,
    "quota__measurement_unit" AS quota_measurement_unit,
    "quota__monetary_unit" AS quota_monetary_unit,
    "quota_definition__description" AS quota_definition_description,
    "quota_definition__validity_start_date" AS quota_definition_validity_start_date,
    "quota_definition__validity_end_date" AS quota_definition_validity_end_date,
    "quota_definition__suspension_periods" AS quota_definition_suspension_periods,
    "quota_definition__blocking_periods" AS quota_definition_blocking_periods,
    "quota_definition__status" AS quota_definition_status,
    "quota_definition__last_allocation_date" AS quota_definition_last_allocation_date,
    CAST("quota_definition__initial_volume" AS DOUBLE) AS quota_definition_initial_volume,
    "quota_definition__balance" AS quota_definition_balance,
    CAST("quota_definition__fill_rate" AS DOUBLE) AS quota_definition_fill_rate
FROM "dbt-uk-trade-quotas--report--quotas-including-current-volumes"
