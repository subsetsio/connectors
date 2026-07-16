-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "month",
    "borough",
    "equipment_type",
    "equipment_code",
    "total_outages",
    "scheduled_outages",
    "unscheduled_outages",
    "entrapments",
    "time_since_major_improvement",
    "am_peak_availability",
    "am_peak_hours_available",
    "am_peak_total_hours",
    "pm_peak_availability",
    "pm_peak_hours_available",
    "pm_peak_total_hours",
    "_24_hour_availability" AS 24_hour_availability,
    "_24_hour_hours_available" AS 24_hour_hours_available,
    "_24_hour_total_hours" AS 24_hour_total_hours,
    "station_name",
    "station_mrn",
    "station_complex_name",
    "station_complex_mrn"
FROM "mta-open-data-rc78-7x78"
