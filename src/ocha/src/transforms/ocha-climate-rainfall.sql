-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Rows mix aggregation periods and administrative levels; filter aggregation_period and admin_level before comparing rainfall values.
SELECT
    "location_code",
    "location_name",
    "admin1_code",
    "admin1_name",
    "admin2_code",
    "admin2_name",
    "admin_level",
    "resource_hdx_id",
    "aggregation_period",
    "provider_admin1_code",
    "provider_admin2_code",
    "rainfall",
    "rainfall_long_term_average",
    "rainfall_anomaly_pct",
    "number_pixels",
    "version",
    "reference_period_start",
    "reference_period_end"
FROM "ocha-climate-rainfall"
