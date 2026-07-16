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
    "stop_code",
    "stop_name",
    "stop_order",
    "passengers_by_car",
    "total_passengers",
    "train_occupancy",
    "car_count",
    "car_capacities",
    "train_capacity",
    "scheduled_time",
    "model",
    "missing_load_data",
    "trip_origin_station",
    "trip_destination_station",
    "trip_origin_station_name",
    "trip_destination_station_1",
    "branch_id",
    "branch_name",
    "pattern_name"
FROM "mta-open-data-hb2b-cimm"
