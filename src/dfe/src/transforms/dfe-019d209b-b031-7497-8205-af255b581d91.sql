-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    CAST("time_period" AS BIGINT) AS time_period,
    "time_identifier",
    "geographic_level",
    "country_code",
    "country_name",
    "region_code",
    "region_name",
    "old_la_code",
    "new_la_code",
    "la_name",
    "phase_type_grouping",
    "attendance_status",
    "attendance_type",
    "attendance_reason",
    "session_count",
    "session_percent"
FROM "dfe-019d209b-b031-7497-8205-af255b581d91"
