-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: No stable row key was verified in the raw profile; use this table as a source snapshot rather than assuming row identity across runs.
SELECT
    "journey_id",
    CAST("capture_time" AS BIGINT) AS capture_time,
    CAST("latitude" AS DOUBLE) AS latitude,
    CAST("longitude" AS DOUBLE) AS longitude,
    CAST("fuzzed_point" AS BOOLEAN) AS fuzzed_point,
    "ignition_status",
    CAST("heading_deg_north" AS DOUBLE) AS heading_deg_north,
    CAST("elevation_ft" AS DOUBLE) AS elevation_ft,
    CAST("speed_mph" AS DOUBLE) AS speed_mph
FROM "u-s-department-of-transportation-f5ku-dn3j"
