-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "id",
    "unit_of_measure",
    "parameter_name",
    "parameter_code",
    "statistic_id",
    "hydrologic_unit_code",
    "state_name",
    CAST("last_modified" AS TIMESTAMP) AS last_modified,
    CAST("begin" AS TIMESTAMP) AS begin,
    CAST("end" AS TIMESTAMP) AS end,
    CAST("begin_utc" AS TIMESTAMP) AS begin_utc,
    CAST("end_utc" AS TIMESTAMP) AS end_utc,
    "computation_period_identifier",
    "computation_identifier",
    "thresholds",
    "sublocation_identifier",
    "primary",
    "monitoring_location_id",
    "web_description",
    "parameter_description",
    "parent_time_series_id",
    "data_gap_interval",
    CAST("_lon" AS DOUBLE) AS lon,
    CAST("_lat" AS DOUBLE) AS lat
FROM "usgs-time-series-metadata"
