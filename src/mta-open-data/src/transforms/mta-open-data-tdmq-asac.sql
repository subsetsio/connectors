-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "stop_path_id",
    "number_of_stops",
    "distance",
    "origin_station_id",
    "destination_station_id",
    "origin_station_name",
    "destination_station_name",
    "station_id",
    "stop_order",
    "line",
    "direction",
    "station_name"
FROM "mta-open-data-tdmq-asac"
