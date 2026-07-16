-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: This table is a latest-field-measurement snapshot; include last_modified when distinguishing revised rows.
SELECT
    "field_measurements_series_id",
    "field_visit_id",
    "parameter_code",
    "monitoring_location_id",
    "observing_procedure_code",
    "observing_procedure",
    CAST("value" AS DOUBLE) AS value,
    "unit_of_measure",
    CAST("time" AS TIMESTAMP) AS time,
    "qualifier",
    "vertical_datum",
    "approval_status",
    "measuring_agency",
    "last_modified",
    "control_condition",
    "measurement_rated",
    CAST("year" AS BIGINT) AS year,
    CAST("month" AS BIGINT) AS month,
    CAST("day" AS BIGINT) AS day,
    "time_of_day",
    CAST("_lon" AS DOUBLE) AS lon,
    CAST("_lat" AS DOUBLE) AS lat,
    "id"
FROM "usgs-latest-field-measurements"
