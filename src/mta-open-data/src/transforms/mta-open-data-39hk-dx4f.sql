-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "gtfs_stop_id",
    "station_id",
    "complex_id",
    "division",
    "line",
    "stop_name",
    "borough",
    "cbd",
    "daytime_routes",
    "structure",
    "gtfs_latitude",
    "gtfs_longitude",
    "north_direction_label",
    "south_direction_label",
    "ada",
    "ada_northbound",
    "ada_southbound",
    "ada_notes",
    "georeference"
FROM "mta-open-data-39hk-dx4f"
