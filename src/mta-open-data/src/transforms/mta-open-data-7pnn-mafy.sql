-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "service_date",
    "service_code",
    "train_id",
    "line",
    "trip_line",
    "direction",
    "stop_order",
    "gtfs_stop_id",
    "arrival_time",
    "departure_time",
    "date_difference",
    "track",
    "division",
    "revenue_service",
    "timepoint",
    "trip_type",
    "path_id",
    "next_trip_type",
    "next_trip_time",
    "supplement_schedule_number",
    "schedule_file_number",
    "origin_gtfs_stop_id",
    "destination_gtfs_stop_id"
FROM "mta-open-data-7pnn-mafy"
