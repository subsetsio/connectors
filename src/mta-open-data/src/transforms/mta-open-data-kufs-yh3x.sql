-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "year",
    "month",
    "timestamp",
    "day_of_week",
    "hour_of_day",
    "route_id",
    "direction",
    "borough",
    "route_type",
    "stop_order",
    "timepoint_stop_id",
    "timepoint_stop_name",
    "timepoint_stop_latitude",
    "timepoint_stop_longitude",
    "next_timepoint_stop_id",
    "next_timepoint_stop_name",
    "next_timepoint_stop_latitude",
    "next_timepoint_stop_longitude",
    "road_distance",
    "average_travel_time",
    "average_road_speed",
    "bus_trip_count",
    "timepoint_stop_georeference",
    "next_timepoint_stop_georeference"
FROM "mta-open-data-kufs-yh3x"
