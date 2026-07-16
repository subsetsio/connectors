-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Peak rows are versioned by last_modified; include it when distinguishing revised peak records.
SELECT
    "time_series_id",
    "monitoring_location_id",
    "parameter_code",
    "unit_of_measure",
    CAST("value" AS DOUBLE) AS value,
    "last_modified",
    "time",
    CAST("water_year" AS BIGINT) AS water_year,
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("day" AS BIGINT) AS day,
    "time_of_day",
    CAST("peak_since" AS BIGINT) AS peak_since,
    "qualifier",
    CAST("_lon" AS DOUBLE) AS lon,
    CAST("_lat" AS DOUBLE) AS lat,
    "id"
FROM "usgs-peaks"
