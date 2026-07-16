-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
-- caution: Published as a full Socrata snapshot table; no stable row key was asserted during schema-only profiling.
SELECT
    "complex_id",
    "is_complex",
    "number_of_stations_in_complex",
    "stop_name",
    "display_name",
    "constituent_station_names",
    "station_ids",
    "gtfs_stop_ids",
    "borough",
    "cbd",
    "daytime_routes",
    "structure_type",
    "latitude",
    "longitude",
    "ada",
    "ada_notes"
FROM "mta-open-data-5f5g-n3cz"
