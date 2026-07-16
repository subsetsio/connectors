-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "time_series_id",
    "monitoring_location_id",
    "parameter_code",
    "statistic_id",
    "time",
    CAST("value" AS DOUBLE) AS value,
    "unit_of_measure",
    "approval_status",
    "qualifier",
    "last_modified",
    CAST("_lon" AS DOUBLE) AS lon,
    CAST("_lat" AS DOUBLE) AS lat,
    "id"
FROM "usgs-continuous"
