-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "unique_trip",
    "service_date",
    "trip_id",
    "trip_id_numeric",
    "direction",
    "scheduled_time_start",
    "scheduled_time_arrive",
    "trip_origin_station_name",
    "trip_destination_station",
    "max_passengers",
    "max_occupancy",
    "car_count",
    "train_capacity",
    "max_stop_name",
    "model",
    "branch_id",
    "branch_name",
    "pattern_name"
FROM "mta-open-data-73th-g5ad"
