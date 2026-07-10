-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "time_frame",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "new_la_code",
    "la_name",
    "old_la_code",
    strptime("reference_date", '%Y-%m-%d')::DATE AS reference_date,
    "education_phase",
    "attendance_status",
    "attendance_type",
    "attendance_reason",
    "session_count",
    "session_percent"
FROM "dfe-63629501-d3ca-c471-9780-ec4cb6fdf172"
