-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "wwtp_jurisdiction",
    CAST("wwtp_id" AS BIGINT) AS wwtp_id,
    "reporting_jurisdiction",
    "sample_location",
    CAST("sample_location_specify" AS BIGINT) AS sample_location_specify,
    "key_plot_id",
    "county_names",
    "county_fips",
    CAST("population_served" AS BIGINT) AS population_served,
    strptime("date_start", '%Y-%m-%d')::DATE AS date_start,
    strptime("date_end", '%Y-%m-%d')::DATE AS date_end,
    CAST("ptc_15d" AS BIGINT) AS ptc_15d,
    CAST("detect_prop_15d" AS BIGINT) AS detect_prop_15d,
    CAST("percentile" AS DOUBLE) AS percentile,
    "sampling_prior",
    strptime("first_sample_date", '%Y-%m-%d')::DATE AS first_sample_date
FROM "cdc-2ew6-ywp6"
