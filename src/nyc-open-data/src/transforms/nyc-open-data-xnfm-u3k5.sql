-- compiled by `hardened compile-transforms` from the measured model
-- profiles (model/tables + columns). Faithful pass-through: verified
-- pure casts only, no data fixes. Regenerate after model-verify;
-- durable edits belong in the model stage, not here.
SELECT
    "work_schedule_project_location_id",
    "borough_name",
    "_day" AS day,
    "date",
    "on_street_name",
    "from_street_name",
    "to_street_name",
    "community_board",
    "area",
    "work_type",
    "crew_type",
    "shift_type",
    "oftcode",
    "location_segment_id",
    "location_wkt",
    "location_node_id"
FROM "nyc-open-data-xnfm-u3k5"
