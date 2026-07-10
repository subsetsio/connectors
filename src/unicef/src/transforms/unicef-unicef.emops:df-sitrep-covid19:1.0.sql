-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows are normalized SDMX observations. Dataflow-specific disaggregations are preserved in the `dimensions` JSON field, so filter those dimensions together with ref_area, indicator, sex, age, time_period, unit_measure, obs_status, and data_source before aggregating.
SELECT
    "ref_area",
    "ref_area_name",
    "indicator",
    "indicator_name",
    "sex",
    "age",
    strptime("time_period", '%Y-%m-%d')::DATE AS time_period,
    CAST("obs_value" AS BIGINT) AS obs_value,
    "unit_measure",
    "obs_status",
    "data_source",
    "lower_bound",
    "upper_bound",
    "dimensions"
FROM "unicef-unicef.emops:df-sitrep-covid19:1.0"
