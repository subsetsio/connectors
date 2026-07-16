-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "schedule_date",
    "day_type",
    "borough",
    "operator",
    "service_id",
    "direction",
    "shape_id",
    "trip_type",
    "route_id",
    "stop_sequence",
    "stop_id",
    "stop_name",
    "schedule_time",
    "origin",
    "destination",
    "school",
    "revenue_stop",
    "timepoint",
    "boarding",
    "alighting",
    "distance_from_start",
    "trip_headsign",
    "block_id",
    "depot_code",
    "bundle"
FROM "mta-open-data-x5mx-4rfs"
