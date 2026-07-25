-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "report_number",
    CAST("report_seq_no" AS BIGINT) AS report_seq_no,
    CAST("dot_number" AS BIGINT) AS dot_number,
    "report_date",
    "report_state",
    CAST("fatalities" AS BIGINT) AS fatalities,
    CAST("injuries" AS BIGINT) AS injuries,
    CAST("tow_away" AS BOOLEAN) AS tow_away,
    CAST("hazmat_released" AS BOOLEAN) AS hazmat_released,
    "trafficway_desc",
    "access_control_desc",
    "road_surface_condition_desc",
    "weather_condition_desc",
    "light_condition_desc",
    "vehicle_id_number",
    "vehicle_license_number",
    "vehicle_license_state",
    CAST("severity_weight" AS BIGINT) AS severity_weight,
    CAST("time_weight" AS BIGINT) AS time_weight,
    "citation_issued_desc",
    CAST("seq_num" AS BIGINT) AS seq_num,
    CAST("not_preventable" AS BOOLEAN) AS not_preventable
FROM "u-s-department-of-transportation-4wxs-vbns"
