-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "division",
    "line",
    "borough",
    "stop_name",
    "complex_id",
    "constituent_station_name",
    "station_id",
    "gtfs_stop_id",
    "daytime_routes",
    "entrance_type",
    "entry_allowed",
    "exit_allowed",
    "entrance_latitude",
    "entrance_longitude",
    "entrance_georeference"
FROM "mta-open-data-i9wp-a4ja"
